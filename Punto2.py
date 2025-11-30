# Instalación de librerías, descomentar si no están instaladas
#!pip install graphviz
#!pip install ipython

from graphviz import Digraph
from IPython.display import display

# Clase nodo binario con atributos para valor, hijo izquierdo y derecho
class Node:
    def __init__(self, value):
        self.value = value      # Valor del nodo (operador o número)
        self.left = None        # Hijo izquierdo
        self.right = None       # Hijo derecho

    def addRight(self, right):  # Asigna hijo derecho
        self.right = right

    def addLeft(self, left):    # Asigna hijo izquierdo
        self.left = left

# Clase para construir y resolver árboles de expresión
class ExpressionTree:

    operators = ["+","-","*","/","^"]  # Operadores permitidos

    def __init__(self, expression : str):
        # Verifica que la expresión tenga paréntesis balanceados
        if not self.__isValid(expression):
            return
        # Construye el árbol a partir de la expresión
        self.root = ExpressionTree.__build(expression)

    @staticmethod
    def __isValid(expression : str):
        # Retorna True si la cantidad de '(' y ')' coincide
        return expression.count("(") == expression.count(")")

    @staticmethod
    def __strip(expresion : str):
        # Elimina paréntesis externos si están de más
        if expresion[0] == "(" and expresion[-1] == ")":
            return expresion[1:-1]
        else:
            return expresion

    @classmethod
    def __isOperand(cls,expression : str):
        # Devuelve True si la expresión NO contiene operadores → es número
        for i in expression:
            if i in cls.operators:
                return False
        return True

    @classmethod
    def __build(cls, expression : str):
        # Caso base: si es un número, se convierte en nodo hoja
        if cls.__isOperand(expression):
            return Node(float(expression))

        # Quita paréntesis innecesarios de la expresión
        expression = cls.__strip(expression)

        # Variable para contar el nivel de paréntesis
        brackets = 0

        # Recorre la expresión para encontrar el operador principal
        for i in range(len(expression)):
            if expression[i] == "(":
                brackets += 1
            elif expression[i] == ")":
                brackets -= 1

            # Cuando brackets == 0 significa que NO está dentro de paréntesis
            elif brackets == 0 and expression[i] in cls.operators:
                nodo = Node(expression[i])  # Crea nodo operador

                # Construye recursivamente lado izquierdo y derecho
                nodo.addLeft(cls.__build(expression[:i]))
                nodo.addRight(cls.__build(expression[i+1:]))

                return nodo

    def solveExpression(self):
        # Resuelve toda la expresión desde la raíz
        return self._solveNode(self.root)

    def _solveNode(self,node):
        # Caso base: si el valor es float, es número → lo retorna
        if isinstance(node.value,float):
            return node.value

        # Según el operador, resuelve recursivamente ambos lados
        elif node.value == "+":
            return self._solveNode(node.left) + self._solveNode(node.right)
        elif node.value == "-":
            return self._solveNode(node.left) - self._solveNode(node.right)
        elif node.value == "*":
            return self._solveNode(node.left) * self._solveNode(node.right)
        elif node.value == "/":
            return self._solveNode(node.left) / self._solveNode(node.right)
        elif node.value == "^":
            return self._solveNode(node.left) ** self._solveNode(node.right)

# Función para visualizar el árbol binario usando graphviz
def visualizar_arbol(arbol):
    dot = Digraph()             # Crea grafo

    # Estilo de los nodos
    dot.attr(
        'node',
        shape='circle',
        style='filled',
        fillcolor='lightblue',
        fontname='Arial',
        fontsize='14'
    )

    def agregar_nodos(node):
        if node is not None:
            node_id = str(id(node))         # ID único para evitar repetición
            dot.node(node_id, str(node.value))

            # Si tiene hijo izquierdo, lo agrega y crea arista
            if node.left is not None:
                hijo_izq_id = str(id(node.left))
                dot.node(hijo_izq_id, str(node.left.value))
                dot.edge(node_id, hijo_izq_id, label='I')  # I = izquierda
                agregar_nodos(node.left)

            # Si tiene hijo derecho, lo agrega y crea arista
            if node.right is not None:
                hijo_der_id = str(id(node.right))
                dot.node(hijo_der_id, str(node.right.value))
                dot.edge(node_id, hijo_der_id, label='D')  # D = derecha
                agregar_nodos(node.right)

    # Si el árbol tiene raíz, inicia la visualización
    if arbol.root is not None:
        agregar_nodos(arbol.root)
        return dot
    else:
        print("El árbol está vacío, no hay nada que dibujar.")
        return None

# Entrada del usuario
expression = input("Ingrese la expresión a calcular: ")

# Construcción del árbol
mi_arbol = ExpressionTree(expression)

# Cálculo de la expresión
respuesta = mi_arbol.solveExpression()

# Visualización del árbol
grafico = visualizar_arbol(mi_arbol)
if grafico:
    display(grafico)

print(f"El resultado de la expresión {expression} es {respuesta}")