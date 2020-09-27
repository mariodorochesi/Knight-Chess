import numpy as np
import copy
import random
import math
from .Casilla import Casilla
from .Action import Action

# Constante que define el tamano del tablero
TAMANO_TABLERO = 8

class State:
    '''
        La clase estado representa distintas variables que definen el
        estado actual en un tiempo determinado, almacenando:
            - Una Matriz donde cada casilla guarda el ID del Caballo y si es enemigo
            o no.
            - La cantidad de caballos aliados.
            - La cantidad de caballos enemigos.
            - La cantidad de caballos aliados siendo atacados.
            - La cantidad de caballos enemigos siendo atacados.
    '''

    me = 1 # Se utiliza como variable para distinguir cuando gano yo
    opponent = -1 # Se utiliza como variable para distinguir cuando gana el oponente

    def __init__(self, enemy_knights_dict, my_knights_dict):
        '''
            Constructor de la clase State.
            Recibe un diccionario de caballos enemigos y un diccionario
            de caballos aliados, y para ellos genera una representacion
            matricial.
        '''
        # Se declara una variable que almacena el tamano del tablero.
        self.tamano = TAMANO_TABLERO
        vCasilla = np.vectorize(Casilla)
        # Se crea matriz inicial de Tamano x Tamano
        init_arr = np.arange(self.tamano*self.tamano).reshape((self.tamano,self.tamano))
        lattice = np.empty((self.tamano,self.tamano), dtype=object)
        lattice[:,:] = vCasilla(init_arr)
        self.tablero = lattice

        # Se posicionan los caballos en el tablero
        for id, position in enemy_knights_dict.items():
            self.tablero[position[0],position[1]] = Casilla(-1,id)
        for id, position in my_knights_dict.items():
            self.tablero[position[0],position[1]] = Casilla(1,id)

        # Se aplica la traspuesta a la matriz para tener una representacion vertical.
        self.tablero = np.transpose(self.tablero)
        # Se definen la cantidad de caballos aliados
        self.caballos_aliados = len(my_knights_dict)
        # Se definen la cantidad de caballos enemigos
        self.caballos_enemigos = len(enemy_knights_dict)
        # El siguiente en mover una pieza soy yo
        self.next_to_move = 1
        # Lista de acciones aplicadas al estado
        self.actions = list()

    def __str__(self):
        '''
            Retorna un String que representa el estado actual
            en donde se muestran las IDS de los caballos o
            null para casillas vacias.
        '''
        string = ""
        for i in range(0,self.tamano):
            for j in range(0,self.tamano):
                string+= self.tablero[i][j].id + " "
            string+="\n"
        return string

    def valid_move(self, action):
        '''
            Funcion para validar que la accion sea posible segun
            las reglas del ajedrez.

            - Considera no traspasar los limites del tablero.
            - No posicionarse en una casilla ya ocupada por un aliado
        '''
        if action.dest_x < 0 or action.dest_y < 0:
            return False
        if action.dest_x > self.tamano-1 or action.dest_y > self.tamano-1:
            return False
        if (not self.tablero[action.dest_x][action.dest_y].is_empty()) and self.tablero[action.dest_x][action.dest_y].is_ally(self.next_to_move):
            return False
        return True

    def get_actions(self, limit = None):
        '''
            Metodo que obtiene una lista de acciones validas
        '''
        actions = list()
        for i in range(0,self.tamano):
            for j in range(0,self.tamano):
                # Para cada casilla, si no esta vacia entonces
                if not self.tablero[i][j].is_empty():
                    if self.next_to_move == 1 and self.tablero[i][j].is_ally(self.next_to_move):
                        movements = [
                            Action(i,j,i-2,j-1,4),
                            Action(i,j,i-1,j-2,5),
                            Action(i,j,i-1,j+2,2),
                            Action(i,j,i-2,j+1,3),
                            Action(i,j,i+1,j-2,6),
                            Action(i,j,i+1,j+2,1),
                            Action(i,j,i+2,j-1,7),
                            Action(i,j,i+2,j+1,0),
                        ]
                        for movement in movements:
                            if self.valid_move(movement):
                                actions.append(movement)
                    elif self.next_to_move == -1 and self.tablero[i][j].is_ally(self.next_to_move):
                        movements = [
                            Action(i,j,i-2,j-1,4),
                            Action(i,j,i-1,j-2,5),
                            Action(i,j,i-1,j+2,2),
                            Action(i,j,i-2,j+1,3),
                            Action(i,j,i+1,j-2,6),
                            Action(i,j,i+1,j+2,1),
                            Action(i,j,i+2,j-1,7),
                            Action(i,j,i+2,j+1,0),
                        ]
                        for movement in movements:
                            if self.valid_move(movement):
                                actions.append(movement)
        if limit is not None:
            returning_actions = list()
            for i in range(limit):
                size = len(actions)
                selected = random.randint(0,size-1)
                state = actions.pop(selected)
                returning_actions.append(state)
            return returning_actions
        return actions  

    def transition(self, action):
        '''
            Recibe una accion y la aplica sobre el estado, retornando
            un nuevo estado.
        '''

        estado_copia = self.copy()
        estado_copia.next_to_move = estado_copia.next_to_move * -1
        if not estado_copia.tablero[action.dest_x][action.dest_y].is_empty():
            if self.next_to_move == 1:
                estado_copia.caballos_enemigos -= 1
            else:
                estado_copia.caballos_aliados -= 1
        estado_copia.tablero[action.dest_x][action.dest_y] = estado_copia.tablero[action.initial_x][action.initial_y]
        estado_copia.tablero[action.initial_x][action.initial_y] = Casilla()
        estado_copia.actions.append(action)
        return estado_copia
        
    def copy(self):
        return copy.deepcopy(self)


    def winner(self):
        '''
            Retorna 1 si yo gano
            Retorna -1 si el oponente gana
            Retorna None cuando aun no hay ganador
        '''
        if self.caballos_aliados == 0:
            return -1

        if self.caballos_enemigos == 0:
            return 1     
        return None

    def game_over(self):
        '''
            Metodo para saber si es que el juego ha finalizado.
        '''
        return self.winner() is not None

    def suggest_move(self):
        # Se obtienen todas las acciones que se pueden generar
        actions = self.get_actions()
        # Se crea una lista con acciones que permiten comer a un enemigo
        confirmed_eating_actions = list()
        # Valor para comparar estados que me permiten comer
        confirmed_eating_val = 0
        # Se crea una lista para acciones que no permiten comer enemigos
        advancing_actions = list()
        # Valor para comparar estados que me permiten avanzar
        advancing_value = 0
        # Se crea una lista para acciones que me permiten salvar mis fichas
        saving_actions = list()
        # Si tiene la posibilidad de comer una pieza entonces que lo haga
        for action in actions:
            if not self.tablero[action.dest_x][action.dest_y].is_empty():
                val = self.eval_eating_action(action)
                if val > confirmed_eating_val:
                    confirmed_eating_val = val
                    confirmed_eating_actions = list()
                    confirmed_eating_actions.append(action)
                elif val == confirmed_eating_val:
                    confirmed_eating_actions.append(action)
        if len(confirmed_eating_actions) > 0:
            return self.transition(random.choice(confirmed_eating_actions))

        # Si tiene la posibilidad de salvar una pieza de ser comida entonces que lo haga
        estado_invertido = self.copy()
        estado_invertido.next_to_move = estado_invertido.next_to_move * -1
        acciones_enemigas = estado_invertido.get_actions()
        for accion_enemiga in acciones_enemigas:
            for action in actions:
                if accion_enemiga.dest_x == action.initial_x and accion_enemiga.dest_y == action.initial_y:
                    is_savable = True
                    for enemy in acciones_enemigas:
                        if action.dest_x == enemy.dest_x and action.dest_y == enemy.dest_y:
                            is_savable = False
                            break
                    if is_savable:
                        saving_actions.append(action)
        if len(saving_actions) > 0:
            return self.transition(random.choice(saving_actions))

        # Prioriza movimientos que avancen en el tablero hacia un posicion ofensiva
        for action in actions:
            if self.next_to_move == 1:
                if action.type in [0,1,7,6] and action.dest_y <=6:
                    val = self.eval_action(action)
                    if val > advancing_value:
                        advancing_value = val
                        advancing_actions = list()
                        advancing_actions.append(action)
                    elif val == advancing_value:
                        advancing_actions.append(action)
            else:
                if action.type in [2,3,4,5] and action.dest_y >= 2:
                    val = self.eval_action(action)
                    if val > advancing_value:
                        advancing_value = val
                        advancing_actions = list()
                        advancing_actions.append(action)
                    elif val == advancing_value:
                        advancing_actions.append(action)
        if len(advancing_actions) > 0:
            return self.transition(random.choice(advancing_actions))
        return self.transition(random.choice(actions))


    def eval_eating_action(self, action):
        '''
            Esta funcion evalua que tan buenos son los movimientos que 
            pueden comer a otro caballo. Para ello avanza una jugada al
            futuro para ver si el enemigo tiene la posibilidad inmediata
            de comer al caballo aliado.
        '''
        # Se genera el estado al que se llegaria al aplicar la transicion
        estado = self.transition(action)
        # Se genera todas las acciones para el estado creado anteriormente
        actions = estado.get_actions()
        value = 1000
        for future_action in actions:
            # Si alguna accion del estado anterior puede comer al caballo entonces se restan 100
            if future_action.dest_x == action.dest_x and future_action.dest_y == action.dest_y:
                value = value - 100
        return value           

    def eval_action(self, action):
        # Se obtienen piezas que estan siendo atacadas
        estado_invertido = self.copy()
        estado_invertido.next_to_move = estado_invertido.next_to_move * -1
        acciones_enemigas = estado_invertido.get_actions()
        atacados = 0
        for action in acciones_enemigas:
            if not self.tablero[action.dest_x][action.dest_y].is_empty():
                atacados = atacados + 1
        # Se genera el estado al que se llegaria al aplicar la transicion
        estado = self.transition(action)
        # Se genera todas las acciones para el estado creado anteriormente
        actions = estado.get_actions()
        value = 1000
        for future_action in actions:
            # Si alguna accion del estado anterior puede comer al caballo entonces se restan 100
            if future_action.dest_x == action.dest_x and future_action.dest_y == action.dest_y:
                value = value - 100
        return value
