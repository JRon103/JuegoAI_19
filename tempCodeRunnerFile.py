    # Crear una nueva ventana para la pantalla de victoria
        pantalla_victoria = pygame.display.set_mode((ANCHO, ALTO))

        # Cargar la imagen de la pantalla de victoria
        pantalla_victoria_img = pygame.image.load('ruta/a/imagen_victoria.png')

        # Dibujar la imagen de la pantalla de victoria en la nueva ventana
        pantalla_victoria.blit(pantalla_victoria_img, (0, 0))

        # Actualizar la nueva ventana
        pygame.display.flip()

        # Esperar un tiempo antes de salir del juego
        pygame.time.wait(5000)  # Esperar 5 segundos (5000 milisegundos)

        pygame.quit()
        sys.exit()