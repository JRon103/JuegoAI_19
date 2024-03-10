import pygame
import sys
import random

# Configuración de pantalla
ANCHO, ALTO = 800, 600
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Persecución y Escape")

# Clase para el perseguidor
class Perseguidor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHO // 2, ALTO // 2)

    def update(self, objetivo):
        dx = objetivo.rect.centerx - self.rect.centerx
        dy = objetivo.rect.centery - self.rect.centery
        distancia = (dx ** 2 + dy ** 2) ** 0.5
        if distancia != 0:
            self.rect.x += dx / distancia
            self.rect.y += dy / distancia

# Clase para el evasor
class Evasor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, ANCHO), random.randint(0, ALTO))

    def update(self):
        self.rect.x += random.randint(-5, 5)
        self.rect.y += random.randint(-5, 5)
        self.rect.x = max(0, min(self.rect.x, ANCHO))
        self.rect.y = max(0, min(self.rect.y, ALTO))

perseguidor = Perseguidor()
evasor = Evasor()

reloj = pygame.time.Clock()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    evasor.update()
    perseguidor.update(evasor)

    pantalla.fill(BLANCO)
    pantalla.blit(perseguidor.image, perseguidor.rect)
    pantalla.blit(evasor.image, evasor.rect)
    pygame.display.flip()
    reloj.tick(30)
