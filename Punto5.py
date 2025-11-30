class Nodo:
    def __init__(self, texto, es_pregunta=False):
        self.texto = texto
        self.es_pregunta = es_pregunta
        self.izq = None
        self.der = None


def preguntar_si_no(msg):
    while True:
        r = input(msg + " (sí/no): ").strip().lower()
        if r in ["si", "sí", "s"]:
            return True
        if r in ["no", "n"]:
            return False
        print("Responde sí o no.")


def jugar(r):
    while True:
        if not preguntar_si_no("¿Estás pensando en un animal?"):
            break

        nodo = r

        while nodo.es_pregunta:
            if preguntar_si_no(nodo.texto):
                nodo = nodo.izq
            else:
                nodo = nodo.der

        if preguntar_si_no(f"¿Es un(a) {nodo.texto}?"):
            print("He acertado.")
            continue
        else:
            print("No conozco ese animal.")

            nuevo = input("¿Cuál era el animal en el que pensabas?: ").strip()
            pregunta = input(
                f"Dame una pregunta sí/no que distinga un(a) {nuevo} de un(a) {nodo.texto}: "
            ).strip()

            resp_correcta = preguntar_si_no(
                f"Para el/la {nuevo}, ¿la respuesta a la pregunta es sí?"
            )

            nuevo_nodo = Nodo(pregunta, es_pregunta=True)
            animal_nuevo = Nodo(nuevo, es_pregunta=False)
            animal_viejo = Nodo(nodo.texto, es_pregunta=False)

            if resp_correcta:
                nuevo_nodo.izq = animal_nuevo
                nuevo_nodo.der = animal_viejo
            else:
                nuevo_nodo.izq = animal_viejo
                nuevo_nodo.der = animal_nuevo

            nodo.texto = nuevo_nodo.texto
            nodo.es_pregunta = True
            nodo.izq = nuevo_nodo.izq
            nodo.der = nuevo_nodo.der


if __name__ == "__main__":
    raiz = Nodo("gato", es_pregunta=False)
    jugar(raiz)