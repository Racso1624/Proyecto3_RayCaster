#Oscar Fernando López Barrios
#Carné 20679
#Gráficas Por Computadora
#Proyecto 3

import pygame
from math import pi
from raycaster import *

#Se inicia la pantalla
pygame.init()
screen = pygame.display.set_mode((1080, 720), pygame.DOUBLEBUF|pygame.HWACCEL|pygame.FULLSCREEN|pygame.HWSURFACE)
screen.set_alpha(None)

#Se crea el raycaster
r = Raycaster(screen)

#Elige el mapa y se carga
map = r.startScreen()
r.load_map(map)

var = True
while True:
    #Se llena la pantalla
    screen.fill((230,230,250))
    r.render()

    r.renderMiniMap()

    #Se muestran los FPS
    font_fps = pygame.font.SysFont('arial', 16)
    fps = "FPS: " + str(round(pygame.time.Clock().tick(30), 3))
    fps_text = font_fps.render(fps, True, (255, 255, 255), (0, 0, 0))
    fps_rect = fps_text.get_rect()
    fps_rect.center = (950, 25)
    screen.blit(fps_text, fps_rect)
    pygame.display.flip()

    #Se toma en cuenta las teclas
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            exit(0)
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_a:
                r.player["direction"] -= pi/10
            elif e.key == pygame.K_d:
                r.player["direction"] += pi/10

            elif e.key == pygame.K_RIGHT:
                r.player["x"] -= 10
            elif e.key == pygame.K_LEFT:
                r.player["x"] += 10
            elif e.key == pygame.K_UP:
                r.player["y"] += 10
            elif e.key == pygame.K_DOWN:
                r.player["y"] -= 10

            if e.key == pygame.K_f:
                if screen.get_flags() and pygame.FULLSCREEN:
                    pygame.display.set_mode((1080, 720))
                else:
                    pygame.display.set_mode((1080, 720),  pygame.DOUBLEBUF|pygame.HWACCEL|pygame.FULLSCREEN)

    #Se verifica si el jugador gana
    if r.playerWin:
        r.gameWin
        var = False