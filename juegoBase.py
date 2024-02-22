import pygame
import sys
import os

# Inicializar Pygame
pygame.init()

# Definición de métodos para los movimientos hacia arriba, abajo, izq y der
def mover (orientacion, steps):

    match orientacion:
        case 'arriba':
            img = 13
        case 'abajo':
            img = 1
        case 'izquierda':
            img = 5
        case 'derecha':
            img = 9
    
    img += (steps % 4)
    
    match lastItem:
        case 0:
            monito_arriba_img = pygame.image.load(os.path.join(ruta_carpeta, 'caminata', f'{img}.png'))
        case 1:
            monito_arriba_img = pygame.image.load(os.path.join(ruta_carpeta, 'caminata_hdmi', f'{img}.png'))
    
    return monito_arriba_img


# Último item tomado (0 = ninguno, 1 = hdmi, ...)
lastItem = 0
lastDirection = ''
numSteps = 0
enemigo1 = 0

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

# Obtener la ruta de la carpeta del script
ruta_carpeta = os.path.dirname(__file__)

# Cargar imágenes del monito para cada dirección
monito_abajo_img = pygame.image.load(os.path.join(ruta_carpeta, 'caminata', '1.png'))
monito_izquierda_img = pygame.image.load(os.path.join(ruta_carpeta, 'caminata', '5.png'))
monito_derecha_img = pygame.image.load(os.path.join(ruta_carpeta, 'caminata', '9.png'))
monito_arriba_img = pygame.image.load(os.path.join(ruta_carpeta, 'caminata', '13.png'))

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
        if lastDirection == "arriba":
            numSteps += 1
        else:
            numSteps = 0
            lastDirection = "arriba"

        monito_img = mover("arriba", numSteps)

    elif direccion == "abajo":
        if lastDirection == "abajo":
            numSteps += 1
        else:
            numSteps = 0
            lastDirection = "abajo"

        monito_img = mover("abajo", numSteps)

    elif direccion == "izquierda":
        if lastDirection == "izquierda":
            numSteps += 1
        else:
            numSteps = 0
            lastDirection = "izquierda"

        monito_img = mover("izquierda", numSteps)

    elif direccion == "derecha":
        if lastDirection == "derecha":
            numSteps += 1
        else:
            numSteps = 0
            lastDirection = "derecha"

        monito_img = mover("derecha", numSteps)

            # Verificar colisión con objetivos
    objetivos_capturados_temp = []  # Lista temporal para almacenar objetivos capturados en este ciclo

    for objetivo in objetivos:
        if (posicion_x, posicion_y) == objetivo:
            objetivos_capturados_temp.append(objetivo)
            lastItem = 1

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

    # Imagen del ENEMIGO
    imagen_obstaculo = pygame.image.load(os.path.join('enemigo2', f'windows{1 + enemigo1 % 10}.png'))
    enemigo1 += 1

    # Dibujar el monito en la pantalla
    pantalla.blit(monito_img, monito_rect)

    # Dibujar la cuadrícula y obstáculos
    for fila in range(CANTIDAD_CASILLAS):
        for columna in range(CANTIDAD_CASILLAS):
            if campo_de_juego[fila][columna] == 1:
                pygame.draw.rect(pantalla, NEGRO, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA, TAMANO_CASILLA, TAMANO_CASILLA))
            elif campo_de_juego[fila][columna] == 2:
                #pygame.draw.rect(pantalla, ROJO, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA, TAMANO_CASILLA, TAMANO_CASILLA))
                pantalla.blit(imagen_obstaculo, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA))
            elif (columna, fila) in objetivos:
                pantalla.blit(objetivo_img, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA))

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de la ejecución
    pygame.time.Clock().tick(10)