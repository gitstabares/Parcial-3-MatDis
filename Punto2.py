#!pip install graphviz
#!pip install ipython
from graphviz import Digraph
from IPython.display import display

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
    def addRight(self, right):
        self.right = right
    def addLeft(self, left):
        self.left = left

class ExpressionTree:
    operators = ["+","-","*","/","^"]
    def __init__(self, expression : str):
        if not self.__isValid(expression):
            return
        self.root = ExpressionTree.__build(expression)
    @staticmethod
    def __isValid(expression : str):
        if expression.count("(") == expression.count(")"):
            return True
        return False
    @staticmethod
    def __strip(expresion : str):
        if expresion[0] == "(" and expresion[-1] == ")":
            return expresion[1:-1]
        else:
            return expresion
        
    @classmethod
    def __isOperand(cls,expression : str):
        for i in cls.operators:
            if i in expression:
                return False
        return True
    
    @classmethod
    def __build(cls, expression : str):
        if cls.__isOperand(expression):
            return Node(float(expression))

        brackets = 0
        for i in range(len(expression)):
            if expression[i] == "(":
                brackets+=1
            elif expression[i] == ")":
                brackets-=1
            elif brackets == 0 and expression[i] in cls.operators:
                nodo = Node(expression[i])
                nodo.addLeft(cls.__build(cls.__strip(expression[:i])))
                nodo.addRight(cls.__build(cls.__strip(expression[i+1:])))
                return nodo
    
    def solveExpression(self):
        return self._solveNode(self.root)

    def _solveNode(self,node):
        if isinstance(node.value,float):
            return node.value
        elif node.value == "+":
            return self._solveNode(node.left)+self._solveNode(node.right)
        elif node.value == "-":
            return self._solveNode(node.left)-self._solveNode(node.right)
        elif node.value == "*":
            return self._solveNode(node.left)*self._solveNode(node.right)
        elif node.value == "/":
            return self._solveNode(node.left)/self._solveNode(node.right)
        elif node.value == "^":
            return self._solveNode(node.left)**self._solveNode(node.right)

expression = input("Ingrese la expresión a calcular: ")
mi_arbol = ExpressionTree(expression)
respuesta = mi_arbol.solveExpression()

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
    def agregar_nodos(node):
        """
        Agrega recursivamente los nodos y sus conexiones al objeto 'dot'.
        """
        if node is not None:
            # Usamos id(nodo) para tener un identificador único en el gráfico
            node_id = str(id(node))

            # Agregamos el nodo al grafo con su valor como etiqueta
            dot.node(node_id, str(node.value))

            # Si existe hijo IZQUIERDO, lo agregamos y dibujamos la flecha
            if node.left is not None:
                hijo_izq_id = str(id(node.left))
                dot.node(hijo_izq_id, str(node.left.value))

                # Conectamos el nodo actual con su hijo izquierdo
                dot.edge(node_id, hijo_izq_id, label='I')  # I = izquierda

                # Llamada recursiva para seguir bajando
                agregar_nodos(node.left)

            # Si existe hijo DERECHO, lo agregamos y dibujamos la flecha
            if node.right is not None:
                hijo_der_id = str(id(node.right))
                dot.node(hijo_der_id, str(node.right.value))

                # Conectamos el nodo actual con su hijo derecho
                dot.edge(node_id, hijo_der_id, label='D')  # D = derecha

                # Llamada recursiva para seguir bajando
                agregar_nodos(node.right)

    # Si el árbol tiene raíz, empezamos a dibujar desde allí
    if arbol.root is not None:
        agregar_nodos(arbol.root)
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
print(f"El resultado de la expresión {expression} es {respuesta}")