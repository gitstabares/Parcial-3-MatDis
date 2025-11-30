class Nodo:
    def __init__(self, texto, es_pregunta=False):
        self.texto = texto                # Contiene la pregunta o el nombre del animal
        self.es_pregunta = es_pregunta    # Indica si este nodo es una pregunta (True) o una respuesta (False)
        self.izq = None                   # Hijo izquierdo (respuesta "sí")
        self.der = None                   # Hijo derecho (respuesta "no")

def preguntar_si_no(msg):
    # Función que fuerza al usuario a responder solo sí o no
    while True:
        r = input(msg + " (sí/no): ").strip().lower()   # Normaliza la entrada del usuario
        if r in ["si", "sí", "s"]:                      # Respuestas afirmativas válidas
            return True
        if r in ["no", "n"]:                            # Respuestas negativas válidas
            return False
        print("Responde sí o no.")                      # Mensaje de error

def jugar(r):
    # r es la raíz del árbol de decisiones
    while True:
        # Pregunta si desea jugar
        if not preguntar_si_no("¿Estás pensando en un animal?"):
            break

        nodo = r  # Comienza desde la raíz del árbol

        # Recorre el árbol mientras el nodo sea una pregunta
        while nodo.es_pregunta:
            if preguntar_si_no(nodo.texto):
                nodo = nodo.izq     # Si la respuesta es sí, va al nodo izquierdo
            else:
                nodo = nodo.der     # Si es no, va al nodo derecho

        # Si llega a un nodo que contiene un animal, intenta adivinarlo
        if preguntar_si_no(f"¿Es un(a) {nodo.texto}?"):
            print("He acertado.")   # El programa acertó
            continue
        else:
            print("No conozco ese animal.")             # No acertó y necesita aprender

            # Se obtiene el nuevo animal pensado por el usuario
            nuevo = input("¿Cuál era el animal en el que pensabas?: ").strip()

            # Se pide una pregunta que distinga ambos animales
            pregunta = input(
                f"Dame una pregunta sí/no que distinga un(a) {nuevo} de un(a) {nodo.texto}: "
            ).strip()

            # Se pide cuál es la respuesta correcta para el nuevo animal
            resp_correcta = preguntar_si_no(
                f"Para el/la {nuevo}, ¿la respuesta a la pregunta es sí?"
            )

            # Se construyen los nuevos nodos
            nuevo_nodo = Nodo(pregunta, es_pregunta=True)   # Nodo pregunta
            animal_nuevo = Nodo(nuevo, es_pregunta=False)   # Nodo animal nuevo
            animal_viejo = Nodo(nodo.texto, es_pregunta=False) # Nodo animal anterior

            # Inserta los nodos según cuál sea la respuesta correcta
            if resp_correcta:
                nuevo_nodo.izq = animal_nuevo   # Sí → animal nuevo
                nuevo_nodo.der = animal_viejo   # No → animal viejo
            else:
                nuevo_nodo.izq = animal_viejo
                nuevo_nodo.der = animal_nuevo

            # Se reemplaza el nodo hoja anterior con la nueva pregunta
            nodo.texto = nuevo_nodo.texto
            nodo.es_pregunta = True
            nodo.izq = nuevo_nodo.izq
            nodo.der = nuevo_nodo.der

if __name__ == "__main__":
    raiz = Nodo("gato", es_pregunta=False)   # Árbol inicial con un solo animal
    jugar(raiz)                               # Inicia el juego