import pygame
from math import pi
from raycaster import *

pygame.init()
screen = pygame.display.set_mode((1080, 720), pygame.DOUBLEBUF|pygame.HWACCEL|pygame.FULLSCREEN|pygame.HWSURFACE)
screen.set_alpha(None)
r = Raycaster(screen)
r.load_map('./map.txt')

c = 0
while True:
    screen.fill((113, 113, 113))
    r.render()

    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            exit(0)
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_a:
                r.player["a"] -= pi/10
            elif e.key == pygame.K_d:
                r.player["a"] += pi/10

            elif e.key == pygame.K_RIGHT:
                r.player["x"] += 10
            elif e.key == pygame.K_LEFT:
                r.player["x"] -= 10
            elif e.key == pygame.K_UP:
                r.player["y"] += 10
            elif e.key == pygame.K_DOWN:
                r.player["y"] -= 10

            if e.key == pygame.K_f:
                if screen.get_flags() and pygame.FULLSCREEN:
                    pygame.display.set_mode((1000, 500))
                else:
                    pygame.display.set_mode((1000, 500),  pygame.DOUBLEBUF|pygame.HWACCEL|pygame.FULLSCREEN)

    pygame.display.flip()