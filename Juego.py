import pygame
import constantes
from Character import Character

pygame.init()

player = Character(50, 50)

window = pygame.display.set_mode((constantes.WINDOW_WIDTH, constantes.WINDOW_HEIGHT))

pygame.display.set_caption("Minimax Arcade")

#Definir variables de movimiento del jugador
mover_arriba = False
mover_abajo = False
mover_izquierda = False
mover_derecha = False

#controlar el frame rate
clock = pygame.time.Clock()

run = True

while run:
    
    clock.tick(constantes.FPS)

    window.fill(constantes.BG_COLOR)

    #Calcular el movimiento del jugador
    delta_x = 0
    delta_y = 0

    if mover_derecha == True:
        delta_x = 5

    if mover_izquierda == True:
        delta_x = -5

    if mover_arriba == True:
        delta_y = -5
    
    if mover_abajo == True:
        delta_y = 5

    #Mover al jugador
    player.movimiento(delta_x, delta_y)


    player.draw(window)


    for event in pygame.event.get():
        #Cierra el juego
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                mover_izquierda = True
            if event.key == pygame.K_d:
                mover_derecha = True
            if event.key == pygame.K_w:
                mover_arriba = True
            if event.key == pygame.K_s:
                mover_abajo = True

    print(f"{delta_x}, {delta_y}")

    pygame.display.update()

pygame.quit()


