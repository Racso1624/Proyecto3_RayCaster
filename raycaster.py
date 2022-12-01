#Oscar Fernando López Barrios
#Carné 20679
#Gráficas Por Computadora
#Proyecto 3

import pygame
from math import pi, cos, sin, atan2

#Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND = (0, 255, 255)

#Se agregan paredes
wall1 = pygame.image.load('./Sprites/wall1.png')
wall2 = pygame.image.load('./Sprites/wall2.png')
wall3 = pygame.image.load('./Sprites/wall2.png')

walls = {
  "1": wall1,
  "2": wall2,
  "3": wall3,
}

#Se agrega jugador
player = pygame.image.load('./Sprites/player.png')

enemies = [
  {
    "x": 150,
    "y": 150,
    "texture": pygame.image.load('./Sprites/sprite1.png')
  },
]

#Se realiza la clase
class Raycaster(object):
  def __init__(self, screen):
    _, _, self.width, self.height = screen.get_rect()
    self.screen = screen
    self.blocksize = 50
    self.player = {
      "x": self.blocksize + 20,
      "y": self.blocksize + 20,
      "direction": pi/3,
      "fov": pi/3
    }
    self.map = []
    self.zbuffer = [999_999 for _ in range(0, int(self.width / 2))]

  #Se realizan los metodos de clear
  def clear(self):
    for x in range(self.width):
      for y in range(self.height):
        r = int((x / self.width) * 255) if x / self.width < 1 else 1
        g = int((y / self.height) * 255) if y / self.height < 1 else 1
        b = 0
        color = (r, g, b)
        self.point(x, y, color)

  #Se carga el mapa
  def load_map(self, filename):
    with open(filename) as f:
      for line in f.readlines():
        self.map.append(list(line))

  def point(self, x, y, c = None):
    self.screen.set_at((x, y), c)

  #Se castea el rayo
  def cast_ray(self, a):

    d = 0

    while True:
      x = self.player["x"] + d * cos(a)
      y = self.player["y"] + d * sin(a)

      i = int(x / self.blocksize)
      j = int(y / self.blocksize)

      if self.map[j][i] != ' ':
        hitx = x - i * self.blocksize
        hity = y - j * self.blocksize

        if 1 < hitx < 49:
          maxhit = hitx
        else:
          maxhit = hity

        tx = int(maxhit * 128 / self.blocksize)

        return d, self.map[j][i], tx

      d += 2

  #Se castea el rayo
  def mini_cast_ray(self, a):

    d = 0

    while True:
      x = int(30 + d * cos(a))
      y = int(self.player["y"] + d * sin(a))

      i = int(x / 20)
      j = int(y / 20)

      if self.map[j][i] != ' ':
        return d, self.map[j][i]

      self.point(x, y, (255,255,255))

      d += 2

  #Se dibuja al player
  def draw_player(self, xi, yi, w = 256, h = 256):
    for i in range(xi, xi + w):
      for j in range(yi, yi + h):

        texture_x = int((i - xi) * 32 / w)
        texture_y = int((j - yi) * 32 / h)
        c = player.get_at((texture_x, texture_y))

        if c != (152, 0, 136, 255):
          self.point(i, j, c)

  #Se renderiza los objetos de la escena
  def draw_rectangle(self, x, y, texture):
    for i in range(x, x + self.blocksize):
      for j in range(y, y + self.blocksize):

        tx = int((i - x) * 128 / self.blocksize)
        ty = int((j - y) * 128 / self.blocksize)

        c = texture.get_at((tx, ty))
        self.point(i, j, c)

  def draw_rectangleMini(self, x, y, texture):
    for i in range(x, x + 20):
      for j in range(y, y + 20):

        tx = int((i - x) * 128 / 20)
        ty = int((j - y) * 128 / 20)

        c = texture.get_at((tx, ty))
        self.point(i, j, c)

  def draw_stake(self, x, h, texture, texture_x):
    start = int((self.height / 2) - h / 2)
    end = int((self.height / 2) + h / 2)

    for y in range(start, end): 
      texture_y = int(((y - start) * 128) / (end - start))
      color = texture.get_at((texture_x, texture_y))
      self.point(x, y, color)

  def draw_sprite(self, sprite):
    sprite_a = atan2(sprite["y"] - self.player["y"], sprite["x"] - self.player["x"])

    sprite_d = ((self.player["x"] - sprite["x"]) ** 2 + (self.player["y"] - sprite["y"]) ** 2) ** (1/2)
    sprite_size = (500 / sprite_d) * 70

    sprite_x = int(self.width / 2) + (sprite_a - self.player["direction"]) * self.height / self.player["fov"] + 250 - sprite_size / 2
    sprite_y = int(self.height / 2) - sprite_size / 2

    sprite_x = int(sprite_x)
    sprite_y = int(sprite_y)
    sprite_size = int(sprite_size)

    for x in range(sprite_x, sprite_x + sprite_size):
      for y in range(sprite_y, sprite_y + sprite_size):
        if 500 < x < 1000 and self.zbuffer[x - 500] >= sprite_d:
          texture_x = int((x - sprite_x) * 128 / sprite_size)
          texture_y = int((y - sprite_y) * 128 / sprite_size)
          c = sprite["texture"].get_at((texture_x, texture_y))
          if c != (152, 0, 136, 255):
            self.point(x, y, c)
            self.zbuffer[x - 500] = sprite_d

  #Se utiliza para renderizar el texto
  def renderText(self, text, font):
    text_s = font.render(text, True, WHITE)
    return text_s, text_s.get_rect()

  #Se renderiza el mapa
  def renderMap(self):
    for i in range(0, 200, 20):
      for j in range(0, 200, 20):
        x = int(i / 20)
        y = int(j / 20)

        if self.map[y][x] != ' ':
          self.draw_rectangleMini(i, j, walls[self.map[y][x]])

  #Funcion para dar la bienvenida y elegir el nivel
  #Se devuelve el nivel deseado por el usuario
  def startScreen(self):

    pygame.mixer.music.load('./Audio/background.mp3')
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play()

    var = True
    while var:
      for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
          exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                var = False

      self.screen.fill(BLACK)

      font_1 = pygame.font.SysFont('arial', 20)
      font_2 = pygame.font.SysFont('arial', 40)

      text_s, text_r = self.renderText(
      "BIENVENIDO AL LABERINTO", font_2)
      text_r.center = (int(self.width / 2), 150)
      self.screen.blit(text_s, text_r)

      text_s, text_r = self.renderText(
      "ESTAS LISTO PARA JUGAR?", font_1)
      text_r.center = (int(self.width / 2), 250)
      self.screen.blit(text_s, text_r)

      text_s, text_r = self.renderText(
      "PRESIONA ESPACIO PARA CONTINUAR", font_1)
      text_r.center = (int(self.width / 2), 350)
      self.screen.blit(text_s, text_r)

      text_s, text_r = self.renderText(
      "PRESIONA ESC PARA SALIR", font_1)
      text_r.center = (int(self.width / 2), 450)
      self.screen.blit(text_s, text_r)

      pygame.display.update()

    var = True
    while var:
      for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
          exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                return './map_1.txt'
            elif event.key == pygame.K_2:
              return './map_2.txt'
            elif event.key == pygame.K_3:
              return './map_3.txt'

      self.screen.fill(BLACK)

      font_1 = pygame.font.SysFont('arial', 20)
      font_2 = pygame.font.SysFont('arial', 40)

      text_s, text_r = self.renderText(
      "ELIGE EL NIVEL QUE DESEES", font_2)
      text_r.center = (int(self.width / 2), 150)
      self.screen.blit(text_s, text_r)

      text_s, text_r = self.renderText(
      "OPCIONES:", font_1)
      text_r.center = (int(self.width / 2), 200)
      self.screen.blit(text_s, text_r)

      text_s, text_r = self.renderText(
      "PRESIONA 1 PARA ELEGIR NIVEL 1", font_1)
      text_r.center = (int(self.width / 2), 250)
      self.screen.blit(text_s, text_r)

      text_s, text_r = self.renderText(
      "PRESIONA 2 PARA ELEGIR NIVEL 2", font_1)
      text_r.center = (int(self.width / 2), 300)
      self.screen.blit(text_s, text_r)

      text_s, text_r = self.renderText(
      "PRESIONA 3 PARA ELEGIR NIVEL 3", font_1)
      text_r.center = (int(self.width / 2), 350)
      self.screen.blit(text_s, text_r)

      text_s, text_r = self.renderText(
      "PRESIONA ESC PARA SALIR", font_1)
      text_r.center = (int(self.width / 2), 450)
      self.screen.blit(text_s, text_r)

      pygame.display.update()

  #Funcion para el fin del juego
  def gameOver(self):

    game_over_sound = pygame.mixer.Sound('./Audio/game_over.mp3')
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(game_over_sound)

    var = True
    while var:
      for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
          exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                var = False

      self.screen.fill((250, 0, 0))

      font = pygame.font.SysFont('arial', 20)
      font_2 = pygame.font.SysFont('arial', 40)

      text_s, text_r = self.renderText(
      "HAS MUERTO", font_2)
      text_r.center = (int(self.width / 2), 250)
      self.screen.blit(text_s, text_r)

      text_s, text_r = self.renderText(
      "PRESIONA ESPACIO PARA JUGAR DE NUEVO", font)
      text_r.center = (int(self.width / 2), 350)
      self.screen.blit(text_s, text_r)

      text_s, text_r = self.renderText(
      "PRESIONA ESC PARA SALIR", font)
      text_r.center = (int(self.width / 2), 450)
      self.screen.blit(text_s, text_r)

      pygame.display.update()

  #Funcion para cuando el usuario gana
  def gameWin(self):

    win_sound = pygame.mixer.Sound('./Audio/win.mp3')
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(win_sound)

    var = True
    while var:
      for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
          exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                var = False
                self.player["x"] = 70
                self.player["y"] = 70

      self.screen.fill((50,205,50))

      font = pygame.font.SysFont('arial', 20)
      font_2 = pygame.font.SysFont('arial', 40)

      text_s, text_r = self.renderText(
      "FELICIDADES! HAS GANADO EL JUEGO", font_2)
      text_r.center = (int(self.width / 2), 250)
      self.screen.blit(text_s, text_r)

      text_s, text_r = self.renderText(
      "PRESIONA ESPACIO PARA JUGAR DE NUEVO", font)
      text_r.center = (int(self.width / 2), 350)
      self.screen.blit(text_s, text_r)

      text_s, text_r = self.renderText(
      "PRESIONA ESC PARA SALIR", font)
      text_r.center = (int(self.width / 2), 450)
      self.screen.blit(text_s, text_r)

      pygame.display.update()

  def playerWin(self):
    return ((350 < self.__player["x"] < 450) and (450 < self.__player["y"] < 500))

  #Se realiza el renderizado de la pantalla
  def render(self):

    for i in range(0, int(self.width)):
      try:
          direction = self.player["direction"] - self.player["fov"] / 2 + self.player["fov"] * i / int(self.width)
          distance, color, texture_x = self.cast_ray(direction)
          x = i
          h = self.height / (distance * cos(direction - self.player["direction"])) * 70
          self.draw_stake(x, h, walls[color], texture_x)
      except:
          self.player["x"] = 70
          self.player["y"] = 70
          self.gameOver()

    for enemy in enemies:
      self.point(enemy["x"], enemy["y"], BLACK)
      self.draw_sprite(enemy)

    self.draw_player(self.width - 256 - 128, self.height - 256)

  def renderMiniMap(self):
    self.renderMap()
    for i in range(0, 200):
      direction = self.player["direction"] - self.player["fov"] / 2+  self.player["fov"] * i / 200
      self.mini_cast_ray(direction)