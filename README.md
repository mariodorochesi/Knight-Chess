# Knight-Chess

Este repositorio considera la implementacion de una función heurística para el juego de búsqueda adversaria **Knight-Chess**.

### Integrantes:
- Gonzalo Tello
- Mario Dorochesi

## **Algoritmo Propuesto**

### **Grafo Implícito**
Inicialmente se modela el problema de **Knight-Chess** como un grafo implícito en donde se define.

- **Estado**: Define una representación del tablero para un momento X en el tiempo. Se guarda dentro de sus valores:
  - Una matriz donde cada casilla representa una casilla del tablero.
  - Cantidad de piezas aliadas
  - Cantidad de piezas enemigas
  - Quien tiene el turno actual

- **Action**: Define el movimiento de una pieza **(x1,y1)** hacia una casilla destino **(x2,y2)**. Además define el número de movimiento según la definición de movimientos de **Braulio Lobo** donde C es el caballo y cada número representa un posible movimiento.

```
     + 4 + 3 +
     5 + + + 2
     + + C + +
     6 + + + 1
     + 7 + 0 +
```

- **Transition**: Define la aplicación de una acción al tablero, es decir el mover un caballo en una posición **(x1,y1)** a una casilla **(x2,y2)** pudiendo en la aplicación de este movimiento comer a un caballo enemigo. Además de moveral caballo cambia también el turno del jugador.

### **Movimiento Sugerido**
El controlador recibe para cada instante de tiempo ***t*** el estado del tablero. Luego de inicializar el estado según la representación de un grafo implícito, llama al método ***suggest_move*** el cual realiza la siguiente lógica.

```
    Para cada accion posible:
        Si la accion permite comer una pieza enemiga entonces la evaluo con eval_eating_action()
            Almaceno en una lista todas las acciones que maximicen eval_eating_action()
            Se retorna una accion aleatoria de la lista
        Sino, si puedo salvar una pieza aliada de ser comida de una pieza enemiga entonces:
            Almaceno en una lista todas las acciones que me permiten salvar una pieza aliada
            Se retorna una accion aleatoria de la lista de acciones para salvar
        Sino, si puedo realizar un movimiento ofensivo la evaluo con eval_action():
            Almaceno en una lista todas las acciones que maximicen eval_action()
            Se retorna una accion aleatoria de la lista movimientos ofensivos
        Retorno movimiento aleatorio
```
Entonces como se puede ver, el metodo ***suggest_move*** retorna para cada instante de tiempo ***t*** una accion a tomar, pasándosela al juego mediante el print de una cadena en formato json.

**Disclamer**: Este repositorio incluye también una implementación de MonteCarlo Tree Search la cual no fue utilizada para la entrega final por los malos resultados obtenidos. **F**