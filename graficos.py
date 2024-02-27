import pygame
import os

# Definición de método para los movimientos hacia arriba, abajo, izq y der
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

# Obtener la ruta de la carpeta del script
ruta_carpeta = os.path.dirname(__file__)

# Cargar imágenes del monito para cada dirección
monito_arriba_img = pygame.image.load(os.path.join(ruta_carpeta, 'caminata', '13.png'))

