class Nodo:
    def __init__(self, valor):
        self.valor = valor

class Pregunta(Nodo):
    def __init__(self, pregunta):
        super().__init__(pregunta)
        self.derecho = None
        self.izquierdo = None

class Animal(Nodo):
    def __init__(self, animal):
        super().__init__(animal)

class Arbol:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        # Caso 1: el árbol está vacío → el nuevo nodo será la raíz
        if self.raiz is None:
            self.raiz = Nodo(valor)
            print(f" {valor} insertado como raíz del árbol")
        else:
            # Caso 2: ya hay raíz → usamos un método auxiliar recursivo
            self._insertar_en(self.raiz, valor)

    def _insertar_en(self, nodo_actual, valor):
        # REGLA: Valores menores van a la IZQUIERDA
        if valor < nodo_actual.valor:
            # Si no hay hijo izquierdo, creamos el nodo aquí
            if nodo_actual.izquierdo is None:
                nodo_actual.izquierdo = Nodo(valor)
                print(f" {valor} insertado a la IZQUIERDA de {nodo_actual.valor}")
            else:
                # Si ya hay hijo izquierdo, seguimos bajando por la izquierda
                self._insertar_en(nodo_actual.izquierdo, valor)

        # REGLA: Valores mayores van a la DERECHA
        elif valor > nodo_actual.valor:
            # Si no hay hijo derecho, creamos el nodo aquí
            if nodo_actual.derecho is None:
                nodo_actual.derecho = Nodo(valor)
                print(f"✅ {valor} insertado a la DERECHA de {nodo_actual.valor}")
            else:
                # Si ya hay hijo derecho, seguimos bajando por la derecha
                self._insertar_en(nodo_actual.derecho, valor)

        # Si el valor ya existe, no lo insertamos para evitar duplicados
        else:
            print(f" {valor} ya existe en el árbol. No se inserta de nuevo.")

def adivinar():
    if 

def main():
    inicio = input("¿Estás pensando en un animal?")
    if inicio.lower() == "no":
        return
    elif inicio.lower() == "si":
        adivinar()