class Casilla:
    '''
        Clase que define cada casilla de la matriz del tablero.
        Para ello se almacena un booleano que define si es aliado
        o no. Tambien se almacena el id del caballo en cuestion.
    '''
    def __init__(self,ally = -1,id = 'null'):
        self.ally = ally
        self.id = id

    def is_empty(self):
        return self.id == 'null'

    def is_ally(self, player):
        return self.ally == player