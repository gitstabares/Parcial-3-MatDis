# Instalación de librerias, descomentar si no están instaladas

#!pip install networkx
#!pip install matplotlib
import networkx as nx
import matplotlib.pyplot as plt 

# Nodos y aristas del grafo
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
    ("E", "F", 3)
]

class UnionFind:
    # Estructura para manejar conjuntos disjuntos
    def __init__(self, n):
        self.padre = {v: v for v in nodos}
        self.rango = [0] * n

    def encontrar(self, x):
        # Encuentra la raíz del conjunto
        if self.padre[x] != x:
            self.padre[x] = self.encontrar(self.padre[x])  # Compresión de caminos
        return self.padre[x]

    def unir(self, x, y):
        # Une dos conjuntos si no generan ciclo
        raiz_x = self.encontrar(x)
        raiz_y = self.encontrar(y)

        if raiz_x == raiz_y:
            return False  # Ya están conectados

        self.padre[raiz_x] = raiz_y
        return True


class Grafo:
    # Grafo no dirigido con pesos
    def __init__(self, num_vertices):
        self.V = num_vertices
        self.aristas = []

    def agregar_arista(self, u, v, peso):
        # Añade arista al grafo
        self.aristas.append((u, v, peso))
        print(f"✓ Arista agregada: {u} ↔ {v} (peso: {peso})")

    def kruskal_mst(self):
        # Algoritmo de Kruskal
        print("\n" + "="*70)
        print(" EJECUTANDO ALGORITMO DE KRUSKAL")
        print("="*70)

        # Ordenar aristas
        aristas_ordenadas = sorted(self.aristas, key=lambda x: x[2])

        print("\nAristas ordenadas:")
        for i, (u, v, peso) in enumerate(aristas_ordenadas, 1):
            print(f"  {i}. {u} ↔ {v} (peso: {peso})")

        uf = UnionFind(self.V)  # Estructura para evitar ciclos
        mst = []
        costo_total = 0
        aristas_agregadas = 0

        for u, v, peso in aristas_ordenadas:
            print(f"\nEvaluando: {u} ↔ {v} (peso: {peso})")
            if uf.unir(u, v):  # Si no genera ciclo
                mst.append((u, v, peso))
                costo_total += peso
                aristas_agregadas += 1
                print(f"   ACEPTADA ({aristas_agregadas}/{self.V - 1})")

                if aristas_agregadas == self.V - 1:
                    print("\n🎉 MST completo.")
                    break
            else:
                print("   RECHAZADA - ciclo")

        return mst, costo_total

    def mostrar_mst(self, mst, costo_total):
        # Imprime resultado final del MST
        print("\n" + "="*70)
        print(" ÁRBOL DE EXPANSIÓN MÍNIMA (MST)")
        print("="*70)

        for i, (u, v, peso) in enumerate(mst, 1):
            print(f"  {i}. {u} ↔ {v} | Peso: {peso}")

        print("\nCosto total:", costo_total)
        print("Aristas en MST:", len(mst))
        print("="*70)


grafo = Grafo(9)
for arista in aristas:
    grafo.agregar_arista(*arista)

mst, costo_total = grafo.kruskal_mst()

print(f"\n✓ Total de conexiones posibles: {len(grafo.aristas)}")
print(f"El costo total mínimo del grafo es: {costo_total}")