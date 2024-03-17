import pygame
import os
import random

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

def tipo_piso (campo, fila, columna):

    imagen_piso = pygame.image.load(os.path.join(ruta_carpeta, 'pisos_pared', 'piso1.png'))

    up = False
    down = False
    left = False
    right = False
    nombre_imagen_obs = 'cruz'

    if campo == 1:
        if campo_con_logica[fila - 1][columna] == 1:
            up = True
        if fila + 1 < max_casillas and campo_con_logica[fila + 1][columna] == 1:
            down = True
        if campo_con_logica[fila][columna - 1] == 1:
            left = True
        if columna + 1 < max_casillas and campo_con_logica[fila][columna + 1] == 1:
            right = True

        if up and not down and left and not right:
            nombre_imagen_obs = 'L_up_izquierda'
        elif up and not down and not left and right:
            nombre_imagen_obs = 'L_up_derecha'
        elif not up and down and left and not right:
            nombre_imagen_obs = 'L_down_izquierda'
        elif not up and down and not left and right:
            nombre_imagen_obs = 'L_down_derecha'
        elif (up or down) and not left and not right:
            nombre_imagen_obs = 'vertical'
        elif (up or down) and left and not right:
            nombre_imagen_obs = 'T_izquierda'
        elif (up or down) and not left and right:
            nombre_imagen_obs = 'T_derecha'
        elif (left or right) and not up and not down:
            nombre_imagen_obs = 'horizontal'
        elif (left or right) and up and not down:
            nombre_imagen_obs = 'T_arriba'
        elif (left or right) and not up and down:
            nombre_imagen_obs = 'T_abajo'
        elif up and down and left and right:
            nombre_imagen_obs = 'cruz'
        else:
            nombre_imagen_obs = 'punto'
        
            

    match campo:
        case 0:
            imagen_piso = pygame.image.load(os.path.join(ruta_carpeta, 'pisos_pared', 'piso1.png'))
        case 1:
            imagen_piso = pygame.image.load(os.path.join(ruta_carpeta, 'pisos_pared', nombre_imagen_obs + '.png'))
        case 2:
            imagen_piso = pygame.image.load(os.path.join(ruta_carpeta, 'water', 'piso2water.png'))
        case 4:
            imagen_piso = pygame.image.load(os.path.join(ruta_carpeta, 'pisos_pared', 'piso4.png'))
    
    return imagen_piso

# Último item tomado (0 = ninguno, 1 = hdmi, ...)
lastItem = 0
lastDirection = ''
numSteps = 0
enemigo1 = 0

campo_con_logica = [[]]
max_casillas = 0

# Obtener la ruta de la carpeta del script
ruta_carpeta = os.path.dirname(__file__)

# Cargar imágenes del monito para cada dirección
monito_arriba_img = pygame.image.load(os.path.join(ruta_carpeta, 'caminata', '13.png'))

objetivo_cable_img = pygame.image.load(os.path.join(ruta_carpeta, 'Objetos', 'c1.png'))

