
class Action:
    '''
        Clase que define una accion a aplicar sobre
        un tablero en Knight-Chess
    '''

    def __init__(self, initial_x, initial_y, dest_x , dest_y, type):
        self.initial_x = initial_x
        self.initial_y = initial_y
        self.dest_x = dest_x
        self.dest_y = dest_y
        self.type = type

    def __str__(self):
        return "X Inicial: {} Y Inicial: {} X Destino : {} Y Destino : {}".format(self.initial_x,self.initial_y,self.dest_x,self.dest_y)