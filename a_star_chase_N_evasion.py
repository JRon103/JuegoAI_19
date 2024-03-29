import pygame
import sys
import os
import graficos
import random
import heapq
import numpy as np


'''
    Tipos de piso en el mapa:

    0: Normal
    1: Obstaculo (Pared, Columnas)
    2: Enemigo
    3: Piso Agua
    
'''

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

'''
    Notas: 
        - Actualmente está evitando los pisos de agua, si esto cambia se debe tomar en cuenta el valor de vida que
        reduce este tipo de piso
        - Lo mismo sucede con los enemigos
'''

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
            if nuevo_estado in visitados or nuevo_estado[0] < 0 or nuevo_estado[1] < 0 or nuevo_estado[0] >= len(mapa) or nuevo_estado[1] >= len(mapa[0]) or mapa[nuevo_estado[1]][nuevo_estado[0]] == 1 or mapa[nuevo_estado[1]][nuevo_estado[0]] == 2:
                continue

            nuevo_nodo = Nodo(nuevo_estado, nodo_actual, nodo_actual.g + 1, distancia_manhattan(nuevo_estado, objetivos[0]))
            heapq.heappush(frontera, (nuevo_nodo.f(), nuevo_nodo))

    return None


class Perseguidor:
    def __init__(self, inicio, evasor):
        self.inicio = inicio
        self.posicion_x, self.posicion_y = inicio
        self.evasor = evasor
        self.camino = None
    
    def actualizar_camino(self, mapa):
        if not self.evasor or not self.evasor.posicion:
            return
        
        self.camino = a_estrella(mapa, (self.posicion_x, self.posicion_y), [self.evasor.posicion])
    
    def mover(self):
        if self.camino:
            if self.posicion_x < self.camino[-1][0]:
                self.posicion_x += 1
            elif self.posicion_x > self.camino[-1][0]:
                self.posicion_x -= 1
            if self.posicion_y < self.camino[-1][1]:
                self.posicion_y += 1
            elif self.posicion_y > self.camino[-1][1]:
                self.posicion_y -= 1
            self.camino.pop()

class Evasor:
    def __init__(self, inicio):
        self.posicion = inicio

# Crear un evasor y perseguidor
evasor = Evasor((random.randrange(0, 15), random.randrange(0, 15)))
perseguidor = Perseguidor((random.randrange(0, 15), random.randrange(0, 15)), evasor)



# Inicializar Pygame
pygame.init()


fuente = pygame.font.SysFont('Arial', 20)
fuente_objetivos = pygame.font.SysFont('Arial', 20)
objetivos_texto = 0

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

# Configurar la pantalla
ANCHO, ALTO = 850, 750
TAMANO_CASILLA = 45
CANTIDAD_CASILLAS = 15
graficos.max_casillas = CANTIDAD_CASILLAS

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Monito Móvil')


# Cargar imagen del objetivo
objetivo_img = pygame.Surface((TAMANO_CASILLA, TAMANO_CASILLA))
objetivo_img = graficos.objetivo_cable_img

# Obtener rectángulo del monito
monito_arriba_img = graficos.monito_arriba_img
monito_rect = monito_arriba_img.get_rect()

# Posición inicial del monito en la cuadrícula
posicion_x, posicion_y =  random.randrange(0,15), random.randrange(0,15)
#posicion_x = 3
#posicion_y = 0
inicio = (posicion_x, posicion_y)
monito_rect.x = posicion_x * TAMANO_CASILLA
monito_rect.y = posicion_y * TAMANO_CASILLA

movimientos = [(posicion_x, posicion_y)]
direcciones = []

# Vidas
vidas = 3

# Dirección inicial del monito
direccion = "arriba"
monito_img = monito_arriba_img

# Configurar velocidad del monito (una casilla por movimiento)
velocidad = TAMANO_CASILLA



# Definir matriz del campo de juego (0: casilla normal, 1: pared, 2: obstáculo)
campo_de_juego = [
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 3, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 3, 3, 3, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 1, 0],
    [0, 0, 0, 2, 0, 0, 0, 3, 0, 3, 3, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 3, 3, 3, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0],
    [0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
]


# ---------
graficos.campo_con_logica = campo_de_juego

# Lista de objetivos (puntos verdes) con coordenadas (x, y)
objetivos = []

for i in range(3):
    obj_ix = random.randrange(0,15)
    obj_iy = random.randrange(0,15)
    objetivos.append((obj_ix, obj_iy))
    campo_de_juego[obj_iy][obj_ix] = 0

objetivosOrg = objetivos

#fix tonto para que donde salga el mono sea una casilla valida
campo_de_juego[posicion_y][posicion_x]=0

mapa = campo_de_juego


# Contador de objetivos capturados
#FIX TONTO, porque se esta sumando de dos en dos
#objetivos_capturados = 0
objetivos_capturados = len(objetivos)*-1

# Creación de caminos disponibles ------------------------- #

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

            if paso:
                if movimientos[len(movimientos) - 1][0] < paso[0]:
                    direcciones.append(4) # derecha
                elif movimientos[len(movimientos) - 1][0] > paso[0]:
                    direcciones.append(2) # izquierda
                elif movimientos[len(movimientos) - 1][1] < paso[1]:
                    direcciones.append(3) # abajo
                elif movimientos[len(movimientos) - 1][1] > paso[1]:
                    direcciones.append(1) # arriba
                
                movimientos.append(paso)

            
    #visualizar_camino(mapa, caminos, objetivos)
else:
    print("No se encontró un camino válido.")

print(direcciones)

# --------------------------------------------------------- #

# Batería ------------------------------------------------- #

'''
    Se manejará con vidas Y baterías / energía ? por mientras así será
'''

bateria = 100.0

i = 0
# Bucle principal
for dir in direcciones:

    if bateria > 0.0:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        #dir = direcciones[i]
        #i+=1
                

        # Actualizar el camino del perseguidor
        perseguidor.actualizar_camino(campo_de_juego)
        
        # Mover el perseguidor
        perseguidor.mover()
                
        # Obtener teclas presionadas
        #teclas = pygame.key.get_pressed()

        # Guardar la posición anterior del monito
        posicion_anterior_x, posicion_anterior_y = posicion_x, posicion_y

        # Mover el monito según las teclas presionadas y dentro de la cuadrícula
        if dir == 2 and posicion_x > 0 and campo_de_juego[posicion_y][posicion_x - 1] != 1:
            posicion_x -= 1
            direccion = "izquierda"
        if dir == 4 and posicion_x < CANTIDAD_CASILLAS - 1 and campo_de_juego[posicion_y][posicion_x + 1] != 1:
            posicion_x += 1
            direccion = "derecha"
        if dir == 1 and posicion_y > 0 and campo_de_juego[posicion_y - 1][posicion_x] != 1:
            posicion_y -= 1
            direccion = "arriba"
        if dir == 3 and posicion_y < CANTIDAD_CASILLAS - 1 and campo_de_juego[posicion_y + 1][posicion_x] != 1:
            posicion_y += 1
            direccion = "abajo"

        # Actualizar la posición del monito en el rectángulo
        monito_rect.x = posicion_x * TAMANO_CASILLA
        monito_rect.y = posicion_y * TAMANO_CASILLA

        if campo_de_juego[posicion_y][posicion_x] == 0:
            bateria -= 1.0
        elif campo_de_juego[posicion_y][posicion_x] == 3:
            bateria -= 1.3

        # Cambiar la imagen del monito según la dirección
        if direccion == "arriba":
            if graficos.lastDirection == "arriba":
                graficos.numSteps += 1
            else:
                graficos.numSteps = 0
                graficos.lastDirection = "arriba"

            monito_img = graficos.mover("arriba", graficos.numSteps)

        elif direccion == "abajo":
            if graficos.lastDirection == "abajo":
                graficos.numSteps += 1
            else:
                graficos.numSteps = 0
                graficos.lastDirection = "abajo"

            monito_img = graficos.mover("abajo", graficos.numSteps)

        elif direccion == "izquierda":
            if graficos.lastDirection == "izquierda":
                graficos.numSteps += 1
            else:
                graficos.numSteps = 0
                graficos.lastDirection = "izquierda"

            monito_img = graficos.mover("izquierda", graficos.numSteps)

        elif direccion == "derecha":
            if graficos.lastDirection == "derecha":
                graficos.numSteps += 1
            else:
                graficos.numSteps = 0
                graficos.lastDirection = "derecha"

            monito_img = graficos.mover("derecha", graficos.numSteps)


        # Verificar colisión con enemigos
        if campo_de_juego[posicion_y][posicion_x] == 2:
            # El jugador ha tocado a un enemigo
            vidas -= 1
            print(f"Oh no! Tocaste a un enemigo. Vidas restantes: {vidas}")

            # Eliminar enemigo de la matriz
            campo_de_juego[posicion_y][posicion_x] = 0  # 0 representa una casilla normal

            # Verificar si el jugador se quedó sin vidas
            if vidas <= 0:
                print("¡Game Over! Te quedaste sin vidas.")
                pygame.quit()
                sys.exit()

                # Verificar colisión con objetivos
        objetivos_capturados_temp = []  # Lista temporal para almacenar objetivos capturados en este ciclo

        for objetivo in objetivos:
            if (posicion_x, posicion_y) == objetivo:
                objetivos_capturados_temp.append(objetivo)
                graficos.lastItem = 1

        # Eliminar objetivos capturados de la lista principal
        objetivos = [objetivo for objetivo in objetivos if objetivo not in objetivos_capturados_temp]

        # Actualizar la lista de objetivos capturados
        objetivos_capturados += len(objetivos_capturados_temp)

        # Limpiar la lista temporal
        objetivos_capturados_temp.clear()

        # Verificar si se han capturado todos los objetivos
        if objetivos_capturados >= len(objetivos):


            print("¡Felicidades! Has capturado todos los objetivos. ¡Ganaste!")

            # Crear una nueva ventana para la pantalla de victoria
            pantalla_victoria = pygame.display.set_mode((480, 270))

            # Cargar la imagen de la pantalla de victoria
            pantalla_victoria_img = pygame.image.load('winScreen.png')

            # Dibujar la imagen de la pantalla de victoria en la nueva ventana
            pantalla_victoria.blit(pantalla_victoria_img, (0, 0))

            # visualizar_camino(mapa, caminos, objetivos)

            # Actualizar la nueva ventana
            pygame.display.flip()

            pygame.quit()
            sys.exit()


        
        # Eliminar objetivos capturados de la lista principal
        objetivos = [objetivo for objetivo in objetivos if (posicion_x, posicion_y) != objetivo]

        # Verificar si se han capturado todos los objetivos
        if objetivos_capturados == len(objetivos):
            print("¡Felicidades! Has capturado todos los objetivos. ¡Ganaste!")
            pygame.quit()
            sys.exit()

        # Limpiar la pantalla
        pantalla.fill(BLANCO)

        # Dibujar el texto de las vidas en la pantalla
        texto_vidas = fuente.render(f'Vidas: {vidas}', True, (0, 0, 0))  # color negro en RGB
        pantalla.blit(texto_vidas, (200, 710))  # Ajusta las coordenadas 

        # Dibujar el texto de objetivos capturados en la pantalla
        texto_objetivos = fuente_objetivos.render(f'Objetivos: {len(objetivos)}', True, (0, 0, 0))
        pantalla.blit(texto_objetivos, (80, 710))

        # Dibujar el texto de las vidas en la pantalla
        texto_bateria = fuente.render(f"Batería: {bateria:.1f}", True, (0, 0, 0))  # color negro en RGB
        pantalla.blit(texto_bateria, (300, 710))  # Ajusta las coordenadas 


        # Imagen del ENEMIGO
        imagen_obstaculo = pygame.image.load(os.path.join('enemigo2', f'windows{1 + graficos.enemigo1 % 10}.png'))
        objetivo_img = pygame.image.load(os.path.join('Objetos', f'c{1 + graficos.enemigo1 % 5}.png'))
        

        # Desplegar imagenes en cada casilla del mapa
        for fila in range(CANTIDAD_CASILLAS):
            for columna in range(CANTIDAD_CASILLAS):

                # Piso normal
                if campo_de_juego[fila][columna] == 0:
                    piso = graficos.tipo_piso(campo_de_juego[fila][columna], fila, columna)
                    pantalla.blit(piso, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA))

                    # Piso + objetivo
                    if (columna, fila) in objetivos:
                        if objetivosOrg.index((columna, fila)) % 2 == 0:
                            objetivo_img = pygame.image.load(os.path.join('Objetos', f'c{1 + graficos.enemigo1 % 5}.png'))  
                        else:                        
                            objetivo_img = pygame.image.load(os.path.join('Objetos', f'm{1 + graficos.enemigo1 % 5}.png'))

                        pantalla.blit(objetivo_img, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA))                


                # Piso normal + objetos
                elif campo_de_juego[fila][columna] == 1:
                    piso = graficos.tipo_piso(campo_de_juego[fila][columna], fila, columna)
                    pantalla.blit(piso, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA))
                    objetivo_img = pygame.image.load(os.path.join('Objetos', f'c{1 + graficos.enemigo1 % 5}.png'))

                # Piso normal + obsatculo
                elif campo_de_juego[fila][columna] == 2:
                    piso = graficos.tipo_piso(0, fila, columna)
                    pantalla.blit(piso, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA))

                    pantalla.blit(imagen_obstaculo, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA))

                # Piso de agua
                elif campo_de_juego[fila][columna] == 3:
                    piso = graficos.tipo_piso(2, fila, columna) 
                    pantalla.blit(piso, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA))

                
                    #pantalla.blit(objetivo_img, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA))

        graficos.enemigo1 += 1
        # Dibujar el monito en la pantalla
        pantalla.blit(monito_img, monito_rect)

        # Actualizar la pantalla
        pygame.display.flip()

        # Controlar la velocidad de la ejecución
        pygame.time.Clock().tick(3)



                    #pygame.draw.rect(pantalla, NEGRO, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA, TAMANO_CASILLA, TAMANO_CASILLA))
                #elif :
                    #pygame.draw.rect(pantalla, ROJO, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA, TAMANO_CASILLA, TAMANO_CASILLA))#el cuadro rojo feo de antes
                    #pantalla.blit(imagen_obstaculo, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA))
    else:
        print("La bateía se ha acabado")
        pygame.quit()
        sys.exit()
