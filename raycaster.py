import pygame
from math import pi, cos, sin, atan2


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND = (0, 255, 255)


wall1 = pygame.image.load('./Sprites/wall1.png')
wall2 = pygame.image.load('./Sprites/wall2.png')
wall3 = pygame.image.load('./Sprites/wall2.png')

walls = {
  "1": wall1,
  "2": wall2,
  "3": wall3,
}

player = pygame.image.load('./Sprites/player.png')

enemies = [
  {
    "x": 150,
    "y": 220,
    "texture": pygame.image.load('./Sprites/sprite1.png')
  },
]

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
    self.zbuffer = [-float('inf') for z in range(0, 500)]

  def clear(self):
    for x in range(self.width):
      for y in range(self.height):
        r = int((x / self.width) * 255) if x / self.width < 1 else 1
        g = int((y / self.height) * 255) if y / self.height < 1 else 1
        b = 0
        color = (r, g, b)
        self.point(x, y, color)

  def load_map(self, filename):
    with open(filename) as f:
      for line in f.readlines():
        self.map.append(list(line))

  def point(self, x, y, c = None):
    self.screen.set_at((x, y), c)

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

      self.point(int(x), int(y), WHITE)

      d += 2

  def draw_player(self, xi, yi, w = 256, h = 256):
    for i in range(xi, xi + w):
      for j in range(yi, yi + h):

        texture_x = int((i - xi) * 32 / w)
        texture_y = int((j - yi) * 32 / h)
        c = player.get_at((texture_x, texture_y))

        if c != (152, 0, 136, 255):
          self.point(i, j, c)

  def draw_rectangle(self, x, y, texture):
    for i in range(x, x + self.blocksize):
      for j in range(y, y + self.blocksize):

        tx = int((i - x) * 128 / self.blocksize)
        ty = int((j - y) * 128 / self.blocksize)

        c = texture.get_at((tx, ty))
        self.point(i, j, c)

  def draw_stake(self, x, h, texture, texture_x):
    start = int(250 - h / 2)
    end = int(250 + h / 2)

    for y in range(start, end): 
      texture_y = int(((y - start) * 128) / (end - start))
      color = texture.get_at((texture_x, texture_y))
      self.point(x, y, color)

  def draw_sprite(self, sprite):
    sprite_a = atan2(sprite["y"] - self.player["y"], sprite["x"] - self.player["x"])

    sprite_d = ((self.player["x"] - sprite["x"]) ** 2 + (self.player["y"] - sprite["y"]) ** 2) ** (1/2)
    sprite_size = (500 / sprite_d) * 70

    sprite_x = 500 + (sprite_a - self.player["direction"])*500/self.player["fov"] + 250 - sprite_size/2
    sprite_y = 250 - sprite_size / 2

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

  def music_background(self):
        pygame.mixer.music.load('./Audio/background.mp3')
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)

  def render_map(self):
    for i in range(0, 500, 50):
      for j in range(0, 500, 50):
        x = int(i / self.blocksize)
        y = int(j / self.blocksize)

        if self.map[y][x] != ' ':
          self.draw_rectangle(i, j, walls[self.map[y][x]])

  def render(self):
    
    self.render_map()
    
    self.point(self.player["x"], self.player["y"], WHITE)

    for i in range(0, 500):
      self.point(500, i, BLACK)
      self.point(501, i, BLACK)
      self.point(499, i, BLACK)

    for i in range(0, 500):
      direction = self.player["direction"] - self.player["fov"] / 2 + self.player["fov"] * i / 500
      distance, color, texture_x = self.cast_ray(direction)
      x = 500 + i
      h = 500 / (distance * cos(direction - self.player["direction"])) * 70
      self.draw_stake(x, h, walls[color], texture_x)
      self.zbuffer[i] = distance

    for enemy in enemies:
      self.point(enemy["x"], enemy["y"], BLACK)
      self.draw_sprite(enemy)

    self.draw_player(1000 - 256 - 128, 500 - 256)