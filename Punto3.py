# Instalación de librerías, descomentar si no están instaladas
#!pip install graphviz
#!pip install ipython

from graphviz import Digraph      # Para dibujar el árbol
from IPython.display import display  # Para mostrarlo en notebooks

# Clase Nodo: representa cada elemento del árbol
class Nodo:
    def __init__(self, valor):
        self.valor = valor                 # Valor almacenado en el nodo
        self.izquierdo = None              # Hijo izquierdo (valores menores)
        self.derecho = None                # Hijo derecho (valores mayores)

# Clase Árbol Binario de Búsqueda
class Arbol:
    def __init__(self):
        self.raiz = None                   # Al inicio el árbol no tiene raíz

    def insertar(self, valor):
        if self.raiz is None:              # Si el árbol está vacío
            self.raiz = Nodo(valor)        # El primer valor se vuelve la raíz
            print(f" {valor} insertado como raíz del árbol")
        else:
            self._insertar_en(self.raiz, valor)  # Llamado recursivo auxiliar
    
    def _insertar_izquierda(self, nodo_actual, valor):
        nodo_actual.izquierdo = Nodo(valor)     # Insertar en la izquierda
        print(f" {valor} insertado a la IZQUIERDA de {nodo_actual.valor}")

    def _insertar_derecha(self, nodo_actual, valor):
        nodo_actual.derecho = Nodo(valor)       # Insertar en la derecha
        print(f" {valor} insertado a la DERECHA de {nodo_actual.valor}")

    def _insertar_en(self, nodo_actual, valor):
        if valor < nodo_actual.valor:           # Si es menor → izquierda
            if nodo_actual.izquierdo is None:   # Crear nodo si no hay hijo
                self._insertar_izquierda(nodo_actual, valor)
            else:
                self._insertar_en(nodo_actual.izquierdo, valor)  # Recursión

        elif valor > nodo_actual.valor:         # Si es mayor → derecha
            if nodo_actual.derecho is None:     # Crear nodo si no hay hijo
                self._insertar_derecha(nodo_actual, valor)
            else:
                self._insertar_en(nodo_actual.derecho, valor)    # Recursión

        else:
            print(f" {valor} ya existe en el árbol. No se inserta de nuevo.") # Evitar duplicados

    def buscar(self, valor):
        return self._buscar_en(self.raiz, valor)    # Búsqueda pública

    def _buscar_en(self, nodo, valor):
        if nodo is None:                            # No encontrado
            return False

        if valor == nodo.valor:                     # Valor encontrado
            return nodo

        elif valor < nodo.valor:                    # Buscar a la izquierda
            return self._buscar_en(nodo.izquierdo, valor)

        else:                                       # Buscar a la derecha
            return self._buscar_en(nodo.derecho, valor)

    def recorrido_inorden(self):
        resultado = []                              # Lista ordenada
        self._inorden_recursivo(self.raiz, resultado)
        return resultado

    def _inorden_recursivo(self, nodo, resultado):
        if nodo is not None:
            self._inorden_recursivo(nodo.izquierdo, resultado)   # Izquierda
            resultado.append(nodo.valor)                         # Nodo
            self._inorden_recursivo(nodo.derecho, resultado)     # Derecha

    def recorrido_preorden(self):
        resultado = []                              # Lista en preorden
        self._preorden_recursivo(self.raiz, resultado)
        return resultado

    def _preorden_recursivo(self, nodo, resultado):
        if nodo is not None:
            resultado.append(nodo.valor)             # Nodo primero
            self._preorden_recursivo(nodo.izquierdo, resultado) # Izquierda
            self._preorden_recursivo(nodo.derecho, resultado)   # Derecha

    def recorrido_postorden(self):
        resultado = []                              # Lista en postorden
        self._postorden_recursivo(self.raiz, resultado)
        return resultado

    def _postorden_recursivo(self, nodo, resultado):
        if nodo is not None:
            self._postorden_recursivo(nodo.izquierdo, resultado) # Izquierda
            self._postorden_recursivo(nodo.derecho, resultado)   # Derecha
            resultado.append(nodo.valor)                         # Nodo al final

# Creamos un árbol nuevo (al inicio está vacío)
mi_arbol = Arbol()

# Lista de números a insertar en el árbol ingresado por nivel
numeros = [12,10,20,7,11,17,27,2,8,14,19,25,29,4,16,22,26,30,23]

# Insertamos cada número de la lista en el árbol
for num in numeros:
    mi_arbol.insertar(num)          # Inserta cada valor siguiendo las reglas del ABB

# Números especiales (No siguen el patrón de ingreso)
mi_arbol._insertar_en(mi_arbol.buscar(11), 9)        # Inserta 9 como hijo según la posición del nodo 11
mi_arbol._insertar_derecha(mi_arbol.buscar(19), "a") # Inserta "a" como hijo derecho del nodo 19
mi_arbol._insertar_izquierda(mi_arbol.buscar(16), "b") # Inserta "b" como hijo izquierdo de 16
mi_arbol._insertar_derecha(mi_arbol.buscar(16), "c")   # Inserta "c" como hijo derecho de 16
mi_arbol._insertar_izquierda(mi_arbol.buscar(22), "d") # Inserta "d" como hijo izquierdo de 22

def visualizar_arbol(arbol):
    """
    Dibuja el árbol binario usando graphviz.
    """

    # Grafo dirigido que representará el árbol
    dot = Digraph(comment='Árbol Binario')

    # Estilo visual de los nodos
    dot.attr(
        'node',
        shape='circle',
        style='filled',
        fillcolor='lightblue',
        fontname='Arial',
        fontsize='14'
    )

    # Función interna para agregar nodos y aristas al grafo
    def agregar_nodos(nodo):
        if nodo is not None:
            nodo_id = str(id(nodo))          # ID único basado en la dirección en memoria
            dot.node(nodo_id, str(nodo.valor))  # Nodo actual

            if nodo.izquierdo is not None:      # Si hay hijo izquierdo
                hijo_izq_id = str(id(nodo.izquierdo))
                dot.node(hijo_izq_id, str(nodo.izquierdo.valor))
                dot.edge(nodo_id, hijo_izq_id, label='I')  # Flecha a izquierda
                agregar_nodos(nodo.izquierdo)

            if nodo.derecho is not None:       # Si hay hijo derecho
                hijo_der_id = str(id(nodo.derecho))
                dot.node(hijo_der_id, str(nodo.derecho.valor))
                dot.edge(nodo_id, hijo_der_id, label='D')  # Flecha a derecha
                agregar_nodos(nodo.derecho)

    # Si el árbol tiene raíz, se dibuja
    if arbol.raiz is not None:
        agregar_nodos(arbol.raiz)
        return dot
    else:
        print(" El árbol está vacío, no hay nada que dibujar.")
        return None

# Visualización del árbol
grafico = visualizar_arbol(mi_arbol)
if grafico:
    display(grafico)     # Muestra el gráfico si existe

# Recorridos del árbol
if mi_arbol:
    print(f"Recorrido en Preorden: {mi_arbol.recorrido_preorden()}")   # Nodo - Izq - Der
    print(f"Recorrido en Inorden: {mi_arbol.recorrido_inorden()}")     # Izq - Nodo - Der
    print(f"Recorrido en Postorden: {mi_arbol.recorrido_postorden()}") # Izq - Der - Nodo
