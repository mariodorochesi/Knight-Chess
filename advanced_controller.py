import random
import json
import sys
from time import sleep
from solver.State import State
from solver.MontecarloTreeSearch import MonteCarloTreeSearch, Node

if __name__ == "__main__":
    state_json = sys.argv[1]

    # Cambiando caracter raro de comillas por doble comillas
    #! Probar si esto funciona en todos los SO
    state_json = state_json.replace(r'\"', '"')

    state_dict = json.loads(state_json)

    state = State(state_dict['enemy_knights_dict'],state_dict['my_knights_dict'])

    #estado = MonteCarloTreeSearch(Node(state)).best_action(2).state

    estado = state.suggest_move()
    accion = estado.actions[-1]
    
    # Creando diccionario de resultado
    result = {
        "knight_id": estado.tablero[accion.dest_x][accion.dest_y].id,
        "knight_movement": accion.type
    }

    # Imprimiendo resultado
    #! Puede que la entrega del resultado tambien tenga que se procesada de la
    #! misma forma que la entrda
    print(json.dumps(result))
