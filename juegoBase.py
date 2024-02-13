import pygame
import sys

# Inicializar Pygame
pygame.init()

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

# Configurar la pantalla
ANCHO, ALTO = 600, 600
TAMANO_CASILLA = 40
CANTIDAD_CASILLAS = 15

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Monito Móvil')

# Cargar imágenes del monito para cada dirección
monito_arriba_img = pygame.image.load('monito_arriba.png')
monito_abajo_img = pygame.image.load('monito_abajo.png')
monito_izquierda_img = pygame.image.load('monito_izquierda.png')
monito_derecha_img = pygame.image.load('monito_derecha.png')

# Cargar imagen del objetivo
objetivo_img = pygame.Surface((TAMANO_CASILLA, TAMANO_CASILLA))
objetivo_img.fill(VERDE)

# Obtener rectángulo del monito
monito_rect = monito_arriba_img.get_rect()

# Posición inicial del monito en la cuadrícula
posicion_x, posicion_y = 1, 1
monito_rect.x = posicion_x * TAMANO_CASILLA
monito_rect.y = posicion_y * TAMANO_CASILLA

# Vidas
vidas = 3

# Dirección inicial del monito
direccion = "arriba"
monito_img = monito_arriba_img

# Configurar velocidad del monito (una casilla por movimiento)
velocidad = TAMANO_CASILLA


# Definir matriz del campo de juego (0: casilla normal, 1: pared, 2: obstáculo)
campo_de_juego = [
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


# Lista de objetivos (puntos verdes) con coordenadas (x, y)
objetivos = [(3, 2), (10, 4), (5, 8)]

# Contador de objetivos capturados
objetivos_capturados = 0

# Bucle principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Obtener teclas presionadas
    teclas = pygame.key.get_pressed()

    # Guardar la posición anterior del monito
    posicion_anterior_x, posicion_anterior_y = posicion_x, posicion_y

    # Mover el monito según las teclas presionadas y dentro de la cuadrícula
    if teclas[pygame.K_LEFT] and posicion_x > 0 and campo_de_juego[posicion_y][posicion_x - 1] != 1:
        posicion_x -= 1
        direccion = "izquierda"
    if teclas[pygame.K_RIGHT] and posicion_x < CANTIDAD_CASILLAS - 1 and campo_de_juego[posicion_y][posicion_x + 1] != 1:
        posicion_x += 1
        direccion = "derecha"
    if teclas[pygame.K_UP] and posicion_y > 0 and campo_de_juego[posicion_y - 1][posicion_x] != 1:
        posicion_y -= 1
        direccion = "arriba"
    if teclas[pygame.K_DOWN] and posicion_y < CANTIDAD_CASILLAS - 1 and campo_de_juego[posicion_y + 1][posicion_x] != 1:
        posicion_y += 1
        direccion = "abajo"

    # Actualizar la posición del monito en el rectángulo
    monito_rect.x = posicion_x * TAMANO_CASILLA
    monito_rect.y = posicion_y * TAMANO_CASILLA

    # Cambiar la imagen del monito según la dirección
    if direccion == "arriba":
        monito_img = monito_arriba_img
    elif direccion == "abajo":
        monito_img = monito_abajo_img
    elif direccion == "izquierda":
        monito_img = monito_izquierda_img
    elif direccion == "derecha":
        monito_img = monito_derecha_img

            # Verificar colisión con objetivos
    objetivos_capturados_temp = []  # Lista temporal para almacenar objetivos capturados en este ciclo

    for objetivo in objetivos:
        if (posicion_x, posicion_y) == objetivo:
            objetivos_capturados_temp.append(objetivo)

    # Eliminar objetivos capturados de la lista principal
    objetivos = [objetivo for objetivo in objetivos if objetivo not in objetivos_capturados_temp]

    # Actualizar la lista de objetivos capturados
    objetivos_capturados += len(objetivos_capturados_temp)

    # Limpiar la lista temporal
    objetivos_capturados_temp.clear()

    # Verificar si se han capturado todos los objetivos
    if objetivos_capturados >= len(objetivos):
        print("¡Felicidades! Has capturado todos los objetivos. ¡Ganaste!")
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

    # Dibujar el monito en la pantalla
    pantalla.blit(monito_img, monito_rect)

    # Dibujar la cuadrícula y obstáculos
    for fila in range(CANTIDAD_CASILLAS):
        for columna in range(CANTIDAD_CASILLAS):
            if campo_de_juego[fila][columna] == 1:
                pygame.draw.rect(pantalla, NEGRO, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA, TAMANO_CASILLA, TAMANO_CASILLA))
            elif campo_de_juego[fila][columna] == 2:
                pygame.draw.rect(pantalla, ROJO, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA, TAMANO_CASILLA, TAMANO_CASILLA))
            elif (columna, fila) in objetivos:
                pantalla.blit(objetivo_img, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA))

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de la ejecución
    pygame.time.Clock().tick(10)