nodos = "ABCDEF"
aristas = [
    ("A", "B", 4),
    ("A", "C", 2),
    ("B", "C", 1),
    ("B", "D", 5),
    ("C", "D", 8),
    ("C", "E", 10),
    ("D", "E", 2),
    ("D", "F", 6),
    ("E", "F", 3)]
class UnionFind:
    """
    Estructura de datos Union-Find (también llamada:
    - Disjoint Set Union (DSU)
    - Conjuntos disjuntos

    Cada vértice pertenece a un conjunto.
    Al comienzo, cada vértice está en su propio conjunto.
    """

    def __init__(self, n):
        """
        Crea la estructura para 'n' elementos (vértices 0, 1, 2, ..., n-1).
        """
        # padre[i] = padre del vértice i.
        # Al inicio, cada vértice es padre de sí mismo ⇢ conjuntos separados.
        self.padre = {v: v for v in nodos}

        # rango[i] ≈ "altura" del árbol que representa al conjunto de i.
        # Se usa para decidir quién cuelga de quién al unir dos conjuntos.
        self.rango = [0] * n

    def encontrar(self, x):
        """
        Encuentra la RAÍZ del conjunto al que pertenece 'x'.

        Si padre[x] == x  → x ES la raíz de su conjunto.
        Si padre[x] != x  → seguimos buscando recursivamente.

        ADEMÁS: Usamos "compresión de caminos":
            - Después de encontrar la raíz,
              hacemos que 'x' apunte DIRECTAMENTE a la raíz.
            - Esto acelera futuras consultas.
        """
        if self.padre[x] != x:
            # Buscamos la raíz del padre de x y comprimimos camino
            self.padre[x] = self.encontrar(self.padre[x])
        return self.padre[x]

    def unir(self, x, y):
        """
        Une los conjuntos a los que pertenecen 'x' e 'y'.

        Devuelve:
            • True  → si se realizó la unión (estaban en conjuntos distintos).
            • False → si ya estaban en el mismo conjunto
                      (o sea, unirlos formaría un ciclo).
        """
        # Buscamos las raíces (representantes) de cada vértice
        raiz_x = self.encontrar(x)
        raiz_y = self.encontrar(y)

        # Si ya tienen la misma raíz, ya estaban conectados → sería ciclo
        if raiz_x == raiz_y:
            return False

        self.padre[raiz_x] = raiz_y
        return True


# ================================================================
#  CLASE GRAFO CON ALGORITMO DE KRUSKAL
# ================================================================
#
# Representaremos el grafo como:
#   - Un número de vértices V (0, 1, 2, ..., V-1)
#   - Una lista de aristas, donde cada arista es una tupla:
#         (u, v, peso)
#   Esto significa: arista que conecta u ↔ v con costo = peso.
# ================================================================

class Grafo:
    """
    Clase que representa un grafo NO dirigido con pesos.

    Implementa:
    - Método para agregar aristas.
    - Algoritmo de Kruskal para construir el MST.
    """

    def __init__(self, num_vertices):
        """
        Crea un grafo con 'num_vertices' vértices.

        Los vértices se numeran de 0 a num_vertices - 1.
        """
        self.V = num_vertices      # Número de vértices
        self.aristas = []          # Lista de aristas (u, v, peso)

    def agregar_arista(self, u, v, peso):
        """
        Agrega una arista NO dirigida entre 'u' y 'v' con el peso dado.

        Args:
            u (int): vértice origen
            v (int): vértice destino
            peso (numérico): costo/peso de la conexión

        Nota: Como el grafo es NO dirigido,
              la arista conecta u ↔ v en ambos sentidos.
        """
        self.aristas.append((u, v, peso))
        print(f"✓ Arista agregada: {u} ↔ {v} (peso: {peso})")

    def kruskal_mst(self):
        """
        Aplica el ALGORITMO DE KRUSKAL para encontrar el MST.

        PASOS RESUMIDOS:
        -----------------
        1. Ordenar todas las aristas por peso (de menor a mayor).
        2. Crear una estructura Union-Find para manejar componentes.
        3. Recorrer las aristas en ese orden:
            - Si la arista conecta dos componentes diferentes:
                • Aceptarla (agregarla al MST).
                • Unir esos componentes en Union-Find.
            - Si la arista conecta vértices que ya están conectados:
                • Rechazarla (formaría un ciclo).
        4. Cuando tengamos (V - 1) aristas aceptadas, el MST está completo.

        Returns:
            mst (lista): lista de aristas (u, v, peso) que forman el MST
            costo_total (numérico): suma de los pesos de esas aristas
        """

        print("\n" + "="*70)
        print(" EJECUTANDO ALGORITMO DE KRUSKAL")
        print("="*70)

        # ------------------------------------------------------------
        # PASO 1: ORDENAR ARISTAS POR PESO (DE MENOR A MAYOR)
        # ------------------------------------------------------------
        print("\n📊 PASO 1: Ordenando aristas por peso...")
        print("-"*70)

        # sorted(...) no modifica la lista original, devuelve una nueva
        aristas_ordenadas = sorted(self.aristas, key=lambda x: x[2])

        print("Aristas ordenadas por peso:")
        for i, (u, v, peso) in enumerate(aristas_ordenadas, 1):
            print(f"  {i}. {u} ↔ {v} (peso: {peso})")

        # ------------------------------------------------------------
        # PASO 2: INICIALIZAR ESTRUCTURA UNION-FIND
        # ------------------------------------------------------------
        print("\n🔧 PASO 2: Inicializando estructura Union-Find...")
        uf = UnionFind(self.V)
        print(f"✓ Estructura Union-Find creada para {self.V} vértices.")

        # ------------------------------------------------------------
        # PASO 3: SELECCIONAR ARISTAS PARA EL MST
        # ------------------------------------------------------------
        print("\n🔍 PASO 3: Seleccionando aristas para el MST...")
        print("-"*70)

        mst = []            # Aquí guardaremos las aristas que sí van al MST
        costo_total = 0     # Suma de los pesos de esas aristas
        aristas_agregadas = 0

        # Recorremos las aristas en orden creciente de peso
        for u, v, peso in aristas_ordenadas:
            print(f"\nEvaluando arista: {u} ↔ {v} (peso: {peso})")

            # Intentamos unir los conjuntos que contienen a u y v
            if uf.unir(u, v):
                #  Se pudieron unir → NO había ciclo → ACEPTAMOS la arista
                mst.append((u, v, peso))
                costo_total += peso
                aristas_agregadas += 1
                print(f"   ACEPTADA - Aristas en MST: {aristas_agregadas}/{self.V - 1}")

                # Si ya tenemos V-1 aristas, el MST está completo
                if aristas_agregadas == self.V - 1:
                    print("\n🎉 ¡MST completo! Ya tenemos todas las aristas necesarias.")
                    break
            else:
                #  No se pudieron unir → ya estaban en el mismo conjunto
                # Incluir esta arista formaría un ciclo, así que la rechazamos.
                print("   RECHAZADA - Formaría un ciclo (los vértices ya estaban conectados)")

        return mst, costo_total

    def mostrar_mst(self, mst, costo_total):
        """
        Muestra el resultado del MST de manera clara y ordenada.

        Args:
            mst (lista): lista de aristas (u, v, peso) del árbol de expansión mínima.
            costo_total (numérico): suma de los pesos de las aristas del MST.
        """
        print("\n" + "="*70)
        print(" ÁRBOL DE EXPANSIÓN MÍNIMA (MST) - RESULTADO FINAL")
        print("="*70)

        print("\n Aristas seleccionadas para el MST:")
        print("-"*70)
        for i, (u, v, peso) in enumerate(mst, 1):
            print(f"  {i}. Vértice {u} ↔ Vértice {v}  |  Peso: {peso}")

        print("\n" + "-"*70)
        print(f" COSTO TOTAL DEL MST: {costo_total}")
        print(f" Número de aristas en el MST: {len(mst)} (debería ser V-1 = {self.V - 1})")
        print(f" Número de vértices conectados: {self.V}")
        print("="*70)


# ================================================================
#  PROGRAMA PRINCIPAL - EJEMPLO PRÁCTICO
# ================================================================
#
# EJEMPLO:
#   - Cada vértice representa una CIUDAD.
#   - Cada arista representa una posible conexión de FIBRA ÓPTICA con un costo.
#   - Queremos conectar TODAS las ciudades gastando lo mínimo posible.
# ================================================================

if __name__ == "__main__":
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "ÁRBOL DE EXPANSIÓN MÍNIMA" + " "*28 + "║")
    print("║" + " "*20 + "Algoritmo de Kruskal" + " "*29 + "║")
    print("╚" + "="*68 + "╝")

    print("\n EJEMPLO: Red de conexión entre ciudades")
    print("-"*70)
    print("Supongamos que queremos conectar 6 ciudades con fibra óptica.")
    print("Cada posible conexión tiene un COSTO (en km de cable, dinero, etc.).")
    print("Objetivo: conectar TODAS las ciudades con el MENOR costo total.\n")

    # Creamos un grafo con 6 vértices (ciudades 0, 1, 2, 3, 4, 5)
    print(" Creando grafo con 6 ciudades (vértices 0 a 5)...")
    print("-"*70)
    grafo = Grafo(9)

    print("\n Agregando conexiones posibles (aristas con sus costos):")
    print("-"*70)

    aristas = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("B", "C", 1),
        ("B", "D", 5),
        ("C", "D", 8),
        ("C", "E", 10),
        ("D", "E", 2),
        ("D", "F", 6),
        ("E", "F", 3)]

    # Agregamos las aristas: (ciudad1, ciudad2, costo)
    for arista in aristas:
        grafo.agregar_arista(*arista)

    print(f"\n✓ Total de conexiones posibles: {len(grafo.aristas)}")

    # Ejecutamos el algoritmo de Kruskal para encontrar el MST
    mst, costo_total = grafo.kruskal_mst()
    import networkx as nx
    import matplotlib.pyplot as plt 
    G = nx.Graph()
    for nodo in nodos:
        G.add_nodes_from(nodo)
    for a,b,costo in aristas:
        G.add_edge(a,b,weight=costo)
    nx.draw(G)
    plt.show()