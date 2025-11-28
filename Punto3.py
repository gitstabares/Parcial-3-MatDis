#!pip install graphviz
#!pip install ipython
from graphviz import Digraph
from IPython.display import display

class Nodo:
    def __init__(self, valor):
        self.valor = valor

        # Hijo izquierdo: aquí irán los valores MENORES que 'valor'
        self.izquierdo = None

        # Hijo derecho: aquí irán los valores MAYORES que 'valor'
        self.derecho = None


# DEFINICIÓN DE LA CLASE ÁRBOL BINARIO DE BÚSQUEDA
# Esta clase administra el árbol completo:
#   - Guarda la referencia a la raíz
#   - Permite insertar valores nuevos
#   - Permite buscar si un valor existe en el árbol
class Arbol:
    def __init__(self):
        # Al principio el árbol está vacío (no hay raíz)
        self.raiz = None

    # -------------------------------
    # MÉTODO: insertar(valor)
    # Inserta un nuevo valor en el árbol, respetando las reglas del ABB:
    #   - Si está vacío, el nuevo valor será la raíz
    #   - Si no, se busca la posición correcta (izquierda o derecha)
    # -------------------------------
    def insertar(self, valor):
        # Caso 1: el árbol está vacío → el nuevo nodo será la raíz
        if self.raiz is None:
            self.raiz = Nodo(valor)
            print(f" {valor} insertado como raíz del árbol")
        else:
            # Caso 2: ya hay raíz → usamos un método auxiliar recursivo
            self._insertar_en(self.raiz, valor)
    
    def _insertar_izquierda(self, nodo_actual, valor):
        nodo_actual.izquierdo = Nodo(valor)
        print(f" {valor} insertado a la IZQUIERDA de {nodo_actual.valor}")

    def _insertar_derecha(self, nodo_actual, valor):
        nodo_actual.derecho = Nodo(valor)
        print(f" {valor} insertado a la DERECHA de {nodo_actual.valor}")
    # -------------------------------
    # MÉTODO AUXILIAR: _insertar_en(nodo_actual, valor)
    # Este método NO lo llama el usuario directamente.
    # Se va moviendo por el árbol:
    #   - Si valor < nodo_actual.valor → va a la izquierda
    #   - Si valor > nodo_actual.valor → va a la derecha
    #   - Si valor == nodo_actual.valor → no se inserta (evita duplicados)
    # -------------------------------
    def _insertar_en(self, nodo_actual, valor):
        # REGLA: Valores menores van a la IZQUIERDA
        if valor < nodo_actual.valor:
            # Si no hay hijo izquierdo, creamos el nodo aquí
            if nodo_actual.izquierdo is None:
                self._insertar_izquierda(nodo_actual, valor)
            else:
                # Si ya hay hijo izquierdo, seguimos bajando por la izquierda
                self._insertar_en(nodo_actual.izquierdo, valor)

        # REGLA: Valores mayores van a la DERECHA
        elif valor > nodo_actual.valor:
            # Si no hay hijo derecho, creamos el nodo aquí
            if nodo_actual.derecho is None:
                self._insertar_derecha(nodo_actual, valor)
            else:
                # Si ya hay hijo derecho, seguimos bajando por la derecha
                self._insertar_en(nodo_actual.derecho, valor)

        # Si el valor ya existe, no lo insertamos para evitar duplicados
        else:
            print(f" {valor} ya existe en el árbol. No se inserta de nuevo.")

    # -------------------------------
    # MÉTODO: buscar(valor)
    # Devuelve True si el valor está en el árbol, False si no.
    # -------------------------------
    def buscar(self, valor):
        return self._buscar_en(self.raiz, valor)

    # -------------------------------
    # MÉTODO AUXILIAR: _buscar_en(nodo, valor)
    # Recorre el árbol recursivamente hasta:
    #   - Encontrar el valor → devuelve True
    #   - Llegar a un hijo vacío (None) → devuelve False
    # -------------------------------
    def _buscar_en(self, nodo, valor):
        # Caso base 1: si el nodo es None, significa que llegamos al "fondo"
        # y no encontramos el valor
        if nodo is None:
            return False

        # Caso base 2: encontramos el valor en el nodo actual
        if valor == nodo.valor:
            return nodo

        # Si el valor es MENOR que el del nodo actual → buscamos a la izquierda
        elif valor < nodo.valor:
            return self._buscar_en(nodo.izquierdo, valor)

        # Si el valor es MAYOR que el del nodo actual → buscamos a la derecha
        else:
            return self._buscar_en(nodo.derecho, valor)

# Creamos un árbol nuevo (al inicio está vacío)
mi_arbol = Arbol()

# Lista de números a insertar en el árbol
numeros = [12,10,20,7,11,17,27,2,8,14,19,25,29,4,16,22,26,30,23]

# Insertamos cada número de la lista en el árbol
for num in numeros:
    mi_arbol.insertar(num)
mi_arbol._insertar_en(mi_arbol.buscar(11),9)
mi_arbol._insertar_derecha(mi_arbol.buscar(16),"c")
mi_arbol._insertar_izquierda(mi_arbol.buscar(16),"b")
mi_arbol._insertar_derecha(mi_arbol.buscar(19),"e")

def visualizar_arbol(arbol):
    """
    Dibuja el árbol binario usando graphviz.

    Parámetro:
        arbol: objeto de la clase Arbol que ya tenga nodos insertados.

    Retorna:
        Un objeto 'Digraph' con el dibujo del árbol.
    """

    # Creamos un nuevo grafo dirigido llamado "Árbol Binario"
    dot = Digraph(comment='Árbol Binario')

    # Configuramos el estilo de los nodos (opcionales, solo para estética)
    dot.attr(
        'node',
        shape='circle',       # Forma circular para cada nodo
        style='filled',       # Que se vea relleno
        fillcolor='lightblue',# Color de relleno
        fontname='Arial',     # Fuente del texto
        fontsize='14'         # Tamaño del texto
    )

    # Función interna (anidada) para agregar nodos y aristas (flechas)
    def agregar_nodos(nodo):
        """
        Agrega recursivamente los nodos y sus conexiones al objeto 'dot'.
        """
        if nodo is not None:
            # Usamos id(nodo) para tener un identificador único en el gráfico
            nodo_id = str(id(nodo))

            # Agregamos el nodo al grafo con su valor como etiqueta
            dot.node(nodo_id, str(nodo.valor))

            # Si existe hijo IZQUIERDO, lo agregamos y dibujamos la flecha
            if nodo.izquierdo is not None:
                hijo_izq_id = str(id(nodo.izquierdo))
                dot.node(hijo_izq_id, str(nodo.izquierdo.valor))

                # Conectamos el nodo actual con su hijo izquierdo
                dot.edge(nodo_id, hijo_izq_id, label='I')  # I = izquierda

                # Llamada recursiva para seguir bajando
                agregar_nodos(nodo.izquierdo)

            # Si existe hijo DERECHO, lo agregamos y dibujamos la flecha
            if nodo.derecho is not None:
                hijo_der_id = str(id(nodo.derecho))
                dot.node(hijo_der_id, str(nodo.derecho.valor))

                # Conectamos el nodo actual con su hijo derecho
                dot.edge(nodo_id, hijo_der_id, label='D')  # D = derecha

                # Llamada recursiva para seguir bajando
                agregar_nodos(nodo.derecho)

    # Si el árbol tiene raíz, empezamos a dibujar desde allí
    if arbol.raiz is not None:
        agregar_nodos(arbol.raiz)
        dot.render('output/Punto3.gv', view=True) # Renders and opens the graph
        return dot
    else:
        print(" El árbol está vacío, no hay nada que dibujar.")
        return None


print("\n Generando visualización gráfica del árbol...")
grafico = visualizar_arbol(mi_arbol)

if grafico:
    # Mostramos el gráfico en la salida de Colab
    display(grafico)
    print("\n ¡Árbol visualizado exitosamente!")
    print("   I = Izquierda | D = Derecha")