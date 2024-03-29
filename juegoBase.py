import time
import pygame
import sys
import os
import graficos
import random
import heapq
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk
'''
    INTELIGENCIA ARTIFICIAL (ENE-JUN 2024 11:00 HRS)

    Desarrolladores:
        - 19130971 FRANCISCO AXEL ROMÁN CARDOZA
        - 20130764 JULIÁN RODOLFO VILLA CRUZ
        - 20130785 IVANOVICX NUÑEZ PEREZ
        - 20130804 ADRIANA SOFÍA SOLIS CASTRO

    
    NOTAS IMPORTANTES PARA EL DESARROLLO / MEJOR ENTENDIMIENTO

    Tipos de piso en el mapa:
        0: Normal
        1: Obstaculo (Pared, Mesas)
        2: Enemigo
        3: Piso de Agua
        4: Área de recarga de batería

    Objetivos:
        - Los objetivos están sobre algun tipo de piso (0 ó 3)
        - No ocupan un tipo de casilla como los Enemigos
    
    Batería:
        - Inicialmente la carga es de 100.0
        - Por cada casilla tipo 0 se descuenta 1.0 y por casilla tipo 3 disminuye 1.3
        - Cuando la batería es menor o igual a 20% buscará la ruta para el centro de carga
        - La batería dejará de cargarse después del 70%
    
'''
FPS=30
# Definir colores
WHITE = (255, 255, 255)
CREAM= (248, 222, 129)
BLACK = (0, 0, 0)
# Definir dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
pygame.init()
# Clases y Métodos ------------------------------------------------------------------------------ #
def show_menu(screen):
    screen.fill(CREAM)
    font = pygame.font.Font(None, 36)
    title_text = font.render("Seleccione con el numero del teclado:", True, BLACK)
    start_text = font.render("1. Iniciar juego", True, BLACK)
    exit_text = font.render("2. Salir", True, BLACK)
    
    screen.blit(title_text, (150, 180))
    screen.blit(start_text, (200, 250))
    screen.blit(exit_text, (200, 300))
    
    pygame.display.flip()
def menu():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Agente Inteligente: Oswi")
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    main()
                
                elif event.key == pygame.K_2:
                    running = False

        show_menu(screen)
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

def main():
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

    def encontrar_posicion_mas_cercana(posicion_actual, posiciones):
        distancia_minima = float('inf')  # Inicializar con un valor grande
        posicion_mas_cercana = None
        
        for posicion in posiciones:
            distancia = distancia_manhattan(posicion_actual, posicion)
            
            if distancia < distancia_minima:
                distancia_minima = distancia
                posicion_mas_cercana = posicion
        
        return posicion_mas_cercana

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
                if nuevo_estado in visitados or nuevo_estado[0] < 0 or nuevo_estado[1] < 0 or nuevo_estado[0] >= len(mapa) or nuevo_estado[1] >= len(mapa[0]) or mapa[nuevo_estado[1]][nuevo_estado[0]] == 1:
                    continue

                nuevo_nodo = Nodo(nuevo_estado, nodo_actual, nodo_actual.g + 1, distancia_manhattan(nuevo_estado, objetivos[0]))
                heapq.heappush(frontera, (nuevo_nodo.f(), nuevo_nodo))

        return None

    def visualizar_camino(mapa, caminos, objetivos):
        mapa_visual = np.array([[0 if cell == 0 else 0.5 for cell in row] for row in mapa])
        for objetivo in objetivos:
            mapa_visual[objetivo[0], objetivo[1]] = 0.8
        
        for i, camino in enumerate(caminos):
            for paso in camino:
                mapa_visual[paso[1], paso[0]] = i + 2
        
        plt.imshow(mapa_visual, cmap='tab10', interpolation='nearest')
        plt.title('Caminos encontrados')
        plt.xticks(range(len(mapa[0])))
        plt.yticks(range(len(mapa)))
        plt.show()

    def buscarCamino (inicio, obj, direcciones):
        camino = a_estrella(campo_de_juego, inicio, obj)
        if camino:
            agregarDirecciones(camino, direcciones)

    def agregarDirecciones(camino, direcciones):
        for i in range(len(camino) - 1):
            paso_actual = camino[i]
            paso_siguiente = camino[i + 1]

            if paso_siguiente[0] > paso_actual[0]:
                direcciones.append(4)  # derecha
            elif paso_siguiente[0] < paso_actual[0]:
                direcciones.append(2)  # izquierda
            elif paso_siguiente[1] > paso_actual[1]:
                direcciones.append(3)  # abajo
            elif paso_siguiente[1] < paso_actual[1]:
                direcciones.append(1)  # arriba

            movimientos.append(paso_actual)

    def terminarJuego(derrota):
        import pygame
        from PIL import Image
        from io import BytesIO
        
        # Inicializar Pygame
        pygame.init()
        
        # Crear una nueva ventana
        pantalla_derrota = pygame.display.set_mode((1140, 810))
        
        # Cargar la imagen de la pantalla de derrota o victoria y redimensionarla
        if derrota:
            image_path = 'loseScreen.png'
        else:
            image_path = 'winScreen.png'
            
        image = Image.open(image_path)
        new_image = image.resize((1140, 810))
        
        # Convertir la imagen de Pillow a bytes
        image_bytes = BytesIO()
        new_image.save(image_bytes, format='PNG')
        image_data = image_bytes.getvalue()
        
        # Convertir la imagen de Pillow a un formato compatible con Pygame
        pygame_image = pygame.image.load(BytesIO(image_data))
        
        # Dibujar la imagen
        pantalla_derrota.blit(pygame_image, (0, 0))
        
        # Actualizar la nueva ventana
        pygame.display.flip()
        
        # Mantener la ventana abierta durante 5 segundos
        pygame.time.delay(5000)
        
        # Finalizar Pygame
        pygame.quit()

    # ----------------------------------------------------------------------------------------------- #
    # Características para el juego ----------------------------------------------------------------- #

    # Inicializar Pygame
    pygame.init()

    fuente = pygame.font.SysFont('Arial', 20)
    fuente_objetivos = pygame.font.SysFont('Arial', 20)
    objetivos_texto = 0

    # Definir colores
    BLANCO = (255, 255, 255)

    # Configurar la pantalla
    ANCHO, ALTO = 850, 750
    TAMANO_CASILLA = 45
    CANTIDAD_CASILLAS = 15
    graficos.max_casillas = CANTIDAD_CASILLAS

    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption('Agente Inteligente')

    # Cargar imagen del objetivo
    objetivo_img = pygame.Surface((TAMANO_CASILLA, TAMANO_CASILLA))
    objetivo_img = graficos.objetivo_cable_img

    # Obtener rectángulo del monito
    monito_arriba_img = graficos.monito_arriba_img
    monito_rect = monito_arriba_img.get_rect()

    # Posición inicial del monito en la cuadrícula
    posicion_x, posicion_y =  random.randrange(0,15), random.randrange(0,15)
    inicio = (posicion_x, posicion_y)
    monito_rect.x = posicion_x * TAMANO_CASILLA
    monito_rect.y = posicion_y * TAMANO_CASILLA

    movimientos = [(posicion_x, posicion_y)]
    direcciones = []

    # Dirección inicial del monito
    direccion = "arriba"
    monito_img = monito_arriba_img

    # Configurar velocidad del monito (una casilla por movimiento)
    velocidad = TAMANO_CASILLA

    # Definir matriz del campo de juego (0: casilla normal, 1: pared, 2: obstáculo)
    campo_de_juego = [
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 3, 3, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 1, 0],
        [0, 1, 1, 1, 0, 0, 0, 3, 3, 3, 3, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 0, 0, 0, 0, 3, 3, 0, 0, 1, 0],
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
   

    graficos.campo_con_logica = campo_de_juego

    # Definición del área de recarga
    area_recarga = []
    obj_ix = random.randrange(2,13)
    obj_iy = random.randrange(2,13)
    area_recarga.append((obj_ix, obj_iy))
    area_recarga.append((obj_ix - 1, obj_iy))
    area_recarga.append((obj_ix - 1, obj_iy - 1))
    area_recarga.append((obj_ix, obj_iy - 1))

    for area_bat in area_recarga:
        campo_de_juego[area_bat[1]][area_bat[0]] = 4

    # Lista de objetivos con coordenadas (x, y)
    objetivos = []
    pisoAguaObjetivos = []

    while len(objetivos) < 25:
        obj_ix = random.randrange(0,15)
        obj_iy = random.randrange(0,15)

        if campo_de_juego[obj_iy][obj_ix] != 4:
            objetivos.append((obj_ix, obj_iy))

            if campo_de_juego[obj_iy][obj_ix] == 3:
                pisoAguaObjetivos.append((obj_iy, obj_ix))
        
            campo_de_juego[obj_iy][obj_ix] = 0

    objetivosOrg = objetivos

    # Definición de la posición de enemigos
    enemigos = []
    pisoAguaEnemigos = []
    while True:
        if len(enemigos) < 3:
            obj_ix = random.randrange(0,15)
            obj_iy = random.randrange(0,15)

            if objetivos.count((obj_ix, obj_iy)) == 0 and campo_de_juego[obj_iy][obj_ix] != 4:
                enemigos.append((obj_ix, obj_iy))

                if campo_de_juego[obj_iy][obj_ix] == 3:
                    pisoAguaEnemigos.append((obj_iy, obj_ix))
                
                campo_de_juego[obj_iy][obj_ix] = 2
            
        else:
            break

    # fix tonto para que donde salga el mono sea una casilla valida
    if campo_de_juego[posicion_y][posicion_x] == 1:
        campo_de_juego[posicion_y][posicion_x] = 0

    # Contador de objetivos capturados
    objetivos_capturados = len(objetivos)*-1

    # ----------------------------------------------------------------------------------------------- #
    # Definición de la 1ra ruta --------------------------------------------------------------------- #
        
    nextObj = encontrar_posicion_mas_cercana((posicion_x, posicion_y), objetivos)
    buscarCamino(inicio, [inicio, nextObj], direcciones)     
    if len(direcciones) == 0:
        print("No se encontró un camino válido")
        main()       

    estado = "Recolectando objetivos"

    # ----------------------------------------------------------------------------------------------- #
    # Características en constante cambio ----------------------------------------------------------- #

    vidas = 3
    bateria = 100.0
    recargar = False
    derrota = False
    victoria = False
    i = 0

    # ----------------------------------------------------------------------------------------------- #
    # Ciclo principal ( Donde se maneja el juego ) -------------------------------------------------- #

    while True:

        # Verificar la batería
        if bateria <= 0.0:
            print("La bateria se ha acabado 1")
            derrota = True
            break
        elif bateria < 20.0:
            print("Bateria baja. Buscando punto de recarga...")
            direcciones = []
            buscarCamino((posicion_x, posicion_y), [(posicion_x, posicion_y), area_recarga[0]], direcciones)
            recargar = True
            estado = "Buscando centro de carga"
            
            casillaInicial = 0
            i = bateria
            while i <= 70.0:
                direcciones.append((casillaInicial % 4) + 1)
                casillaInicial += 1
                i += 3.0

        # Empezar el recorrido
        for dir in direcciones:
            if bateria > 0.0:

                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                
                
                # Guardar la posición anterior del monito ---------------------------------------------
                posicion_anterior_x, posicion_anterior_y = posicion_x, posicion_y

                # Mover el monito según la dirección, dentro del campo de juego -----------------------
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

                # Si estamos en modo de recarga, checará lo siguiente
                if recargar:
                    if campo_de_juego[posicion_y][posicion_x] == 4:
                        if bateria >= 70.0:
                            recargar = False
                            estado = "Recolectando Objetivos"
                            break
                        else:
                            bateria += 3.0
                            estado = "Recargando batería"
                else:
                    estado = "Recolectando objetivos"


                # Actualizar la posición del monito en el rectángulo ----------------------------------
                monito_rect.x = posicion_x * TAMANO_CASILLA
                monito_rect.y = posicion_y * TAMANO_CASILLA

                # Cambiar la imagen del monito según la dirección -------------------------------------
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

                # Verificar colisión con enemigos -----------------------------------------------------
                if campo_de_juego[posicion_y][posicion_x] == 2:
                    vidas -= 1
                    print(f"Oh no! Tocaste a un enemigo. Vidas restantes: {vidas}")

                    # Eliminar enemigo de la matriz
                    if pisoAguaEnemigos.count((posicion_y, posicion_x)) > 0:
                        campo_de_juego[posicion_y][posicion_x] = 3
                    else:
                        campo_de_juego[posicion_y][posicion_x] = 0

                    # Verificar si el jugador se quedó sin vidas
                    if vidas <= 0:
                        print("¡Game Over! Te quedaste sin vidas.")
                        derrota = True
                    
                # Lista temporal para almacenar objetivos capturados en este ciclo --------------------
                objetivos_capturados_temp = []  

                for objetivo in objetivos:
                    if (posicion_x, posicion_y) == objetivo:
                        objetivos_capturados_temp.append(objetivo)
                        objetivos.remove((posicion_x, posicion_y))
                        graficos.lastItem = 1
                
                # Eliminar objetivos capturados de la lista principal
                objetivos = [objetivo for objetivo in objetivos if objetivo not in objetivos_capturados_temp]

                # Actualizar la lista de objetivos capturados
                objetivos_capturados += len(objetivos_capturados_temp)

                # Limpiar la lista temporal
                objetivos_capturados_temp.clear()

                # Verificar si se han capturado todos los objetivos
                if len(objetivos)<=0:
                    print("Felicidades! Has capturado todos los objetivos. Ganaste!")
                    victoria = True
                
                # Eliminar objetivos capturados de la lista principal
                objetivos = [objetivo for objetivo in objetivos if (posicion_x, posicion_y) != objetivo]

                # Imagen del ENEMIGO ------------------------------------------------------------------
                imagen_obstaculo = pygame.image.load(os.path.join('enemigo1', f'android{1 + graficos.enemigo1 % 10}.png'))
                objetivo_img = pygame.image.load(os.path.join('Objetos', f'c{1 + graficos.enemigo1 % 5}.png'))

                if campo_de_juego[posicion_y][posicion_x] == 0:
                    bateria -= 1.0
                elif campo_de_juego[posicion_y][posicion_x] == 3:
                    bateria -= 1.3
                
                # Limpiar la pantalla -----------------------------------------------------------------
                pantalla.fill(BLANCO)

                # Dibujar el texto de las vidas en la pantalla
                texto_vidas = fuente.render(f'Vidas: {vidas}', True, (0, 0, 0))
                pantalla.blit(texto_vidas, (200, 710))  # Ajusta las coordenadas 

                # Dibujar el texto de objetivos capturados en la pantalla
                texto_objetivos = fuente_objetivos.render(f'Objetivos: {len(objetivos)}', True, (0, 0, 0))
                pantalla.blit(texto_objetivos, (80, 710))

                # Dibujar el texto de la batería
                texto_bateria = fuente.render(f"Batería: {0.0 if bateria <= 0.0 else bateria:.1f}", True, (0, 0, 0))
                pantalla.blit(texto_bateria, (300, 710))

                # Dibujar el texto del estado 
                texto_estado = fuente.render(f"Estado: {estado}", True, (0, 0, 0))
                pantalla.blit(texto_estado, (500, 710))

                # Desplegar imagenes en cada casilla del mapa -----------------------------------------
                for fila in range(CANTIDAD_CASILLAS):
                    for columna in range(CANTIDAD_CASILLAS):

                        # Piso normal
                        if campo_de_juego[fila][columna] == 0:
                            piso = graficos.tipo_piso(campo_de_juego[fila][columna], fila, columna)

                            if pisoAguaObjetivos.count((fila, columna)) > 0:
                                piso = graficos.tipo_piso(2, fila, columna)

                            pantalla.blit(piso, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA))

                            # Piso + objetivo
                            if (columna, fila) in objetivos:
                                if objetivosOrg.index((columna, fila)) % 2 == 0:
                                    objetivo_img = pygame.image.load(os.path.join('Objetos', f'c{1 + graficos.enemigo1 % 5}.png'))  
                                else:                        
                                    objetivo_img = pygame.image.load(os.path.join('Objetos', f'm{1 + graficos.enemigo1 % 5}.png'))

                                pantalla.blit(objetivo_img, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA))                


                        # Obstaculos
                        elif campo_de_juego[fila][columna] == 1:
                            piso = graficos.tipo_piso(campo_de_juego[fila][columna], fila, columna)
                            pantalla.blit(piso, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA))
                            objetivo_img = pygame.image.load(os.path.join('Objetos', f'c{1 + graficos.enemigo1 % 5}.png'))

                        # Enemigos
                        elif campo_de_juego[fila][columna] == 2:

                            piso = graficos.tipo_piso(0, fila, columna)

                            if pisoAguaEnemigos.count((fila, columna)) > 0:
                                piso = graficos.tipo_piso(2, fila, columna)
                            
                            pantalla.blit(piso, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA))

                            pantalla.blit(imagen_obstaculo, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA))

                        # Piso de agua
                        elif campo_de_juego[fila][columna] == 3:
                            piso = graficos.tipo_piso(2, fila, columna) 
                            pantalla.blit(piso, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA))

                            #pantalla.blit(objetivo_img, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA))
                        
                        # Área de recarga
                        elif campo_de_juego[fila][columna] == 4:
                            piso = graficos.tipo_piso(4, fila, columna)
                            pantalla.blit(piso, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA))

                graficos.enemigo1 += 1
                
                # Dibujar el monito en la pantalla
                pantalla.blit(monito_img, monito_rect)

                # Actualizar la pantalla
                pygame.display.flip()

                # Velocidad de la ejecución
                pygame.time.Clock().tick(5)

                if derrota:
                    time.sleep(2)
                    terminarJuego(True)
                elif victoria:
                    time.sleep(2)
                    terminarJuego(False)

            else:
                print("La bateria se ha acabado 2")
                derrota = True
                break          
        
        # Fin del las direcciones (ciclo For)
        direcciones = []

        if len(objetivos) > 0:
            nextObj = encontrar_posicion_mas_cercana((posicion_x, posicion_y), objetivos)    
            buscarCamino((posicion_x, posicion_y), [(posicion_x, posicion_y), nextObj], direcciones)
            estado = "Recolectando objetivos"

        if len(direcciones) == 0: 
            print("el juego se rompio inesperadamente")
            main()               
            break

    if derrota:
        time.sleep(2)
        terminarJuego(True)
menu()
# Fin del juego -----------------------------------------------------------------------------------