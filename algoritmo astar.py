import heapq
import matplotlib.pyplot as plt
import numpy as np

class Nodo:
    def __init__(self, estado, padre=None, g=0, h=0):
        self.estado = estado
        self.padre = padre
        self.g = g  # Costo acumulado desde el inicio hasta este nodo
        self.h = h  # Heurística (estimación del costo restante hasta el objetivo)
    
    def f(self):
        return self.g + self.h

    def __lt__(self, other):
        return self.f() < other.f()

def distancia_manhattan(origen, destino):
    return abs(destino[0] - origen[0]) + abs(destino[1] - origen[1])

def a_estrella(mapa, inicio, objetivos):
    frontera = []
    heapq.heappush(frontera, (0, Nodo(inicio)))  # Prioridad, Nodo
    visitados = set()

    while frontera:
        _, nodo_actual = heapq.heappop(frontera)

        if nodo_actual.estado in objetivos:
            objetivos.remove(nodo_actual.estado)
            if not objetivos:
                camino = []
                while nodo_actual:
                    camino.append(nodo_actual.estado)
                    nodo_actual = nodo_actual.padre
                return camino[::-1]

        visitados.add(nodo_actual.estado)

        for movimiento in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nuevo_estado = (nodo_actual.estado[0] + movimiento[0], nodo_actual.estado[1] + movimiento[1])
            if nuevo_estado in visitados or nuevo_estado[0] < 0 or nuevo_estado[1] < 0 or nuevo_estado[0] >= len(mapa) or nuevo_estado[1] >= len(mapa[0]) or mapa[nuevo_estado[0]][nuevo_estado[1]] == 1:
                continue

            nuevo_nodo = Nodo(nuevo_estado, nodo_actual, nodo_actual.g + 1, distancia_manhattan(nuevo_estado, objetivos[0]))
            heapq.heappush(frontera, (nuevo_nodo.f(), nuevo_nodo))

    return None

def visualizar_camino(mapa, caminos, objetivos):
    mapa_visual = np.array([[0 if cell == 0 else 0.5 for cell in row] for row in mapa])
    for objetivo in objetivos:
        mapa_visual[objetivo[0], objetivo[1]] = 0.8
    
    colores = ['red', 'green', 'blue']
    for i, camino in enumerate(caminos):
        for paso in camino:
            mapa_visual[paso[0], paso[1]] = i + 2
    
    plt.imshow(mapa_visual, cmap='tab10', interpolation='nearest')
    plt.title('Caminos encontrados')
    plt.xticks(range(len(mapa[0])))
    plt.yticks(range(len(mapa)))
    plt.gca().invert_yaxis()
    plt.show()

# Matriz proporcionada
mapa = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 3, 3, 3, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

inicio = (0, 0)  # Cambiado a (0, 0) para la esquina superior izquierda
objetivos = [(3, 2), (10, 4), (5, 8)]  # Agregados múltiples objetivos según tus indicaciones

caminos = []
for objetivo in objetivos:
    camino = a_estrella(mapa, inicio, [objetivo])
    if camino:
        caminos.append(camino)
        inicio = objetivo

if caminos:
    print("Caminos encontrados:")
    for i, camino in enumerate(caminos):
        print(f"Camino {i+1}:")
        for paso in camino:
            print(paso)
    visualizar_camino(mapa, caminos, objetivos)
else:
    print("No se encontró un camino válido.")
