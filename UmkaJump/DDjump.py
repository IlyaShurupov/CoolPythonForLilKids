
import pygame
import random
import tkinter as tk
import time
import os

def time_ms():
    return int(round(time.time() * 1000))

# ------------------- 

class Drawer():
  screen = None
  size = (500, 700)
  font = None
  color_clear = (0, 0, 0)
  color1 = (255, 0, 0)
  color2 = (0, 0, 0)

  textures = {
    "tile" : pygame.image.load("tile.png"),
    "person" : pygame.image.load("person.png"),

    "booster" : pygame.image.load("booster.png"),
    "tile_broken1" : pygame.image.load("tile_broken1.png"),
    "tile_broken2" : pygame.image.load("tile_broken2.png"),
    "tile_broken3" : pygame.image.load("tile_broken3.png"),
  }

  def __init__(self) -> None:
      pygame.init()
      pygame.font.init()
      # Set the size of the window
      
      self.font = pygame.font.SysFont('Comic Sans MS', 30)
      self.screen = pygame.display.set_mode(self.size)

  def drawText(self, text, pos):
      tex = self.font.render(text, False, (255, 255, 255))
      self.screen.blit(tex, pos)
      pass

  def drawRect(self, rect):
      pygame.draw.rect(self.screen, self.color1, (rect.x, self.size[1] - rect.y - rect.h, rect.w, rect.h))
  
  def startDraw(self):
      self.screen.fill(self.color_clear)

  def drawTex(self, id, rect):
    image = self.textures[id]
    scaled = pygame.transform.smoothscale(image, (rect.w, rect.h))
    dst_rect = pygame.Rect(rect.x, self.size[1] - rect.y - rect.h, rect.w, rect.h)
    self.screen.blit(scaled, dst_rect)

  def endDraw(self):
      # Update the screen
      pygame.display.flip()
 
  def __del__(self):
      # Close the window and quit.
      pygame.quit()

class Rect():
    x = 0.0
    y = 0.0
    w = 0.0
    h = 0.0

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        pass

class Person():
    y_vel_max = 6.2
    x_vel_max = 10

    def __init__(self):
      self.rect = Rect(0, 0, 40, 80)
      self.x_vel = 0
      self.y_vel = self.y_vel_max

class Floor():

    def __init__(self, rect = Rect(0, 0, 100, 20)):
        self.rect = rect
        self.moveable = bool(random.choices([0, 1], weights=[0.8, 0.2])[0])
        self.move_range = random.uniform(0.5, 1) * 300
        self.starting_x = self.rect.x
        self.move_dir_left = bool(random.choices([0, 1], weights=[0.5, 0.5])[0])
        self.move_speed = random.uniform(0.5, 2)
        self.booster = bool(random.choices([0, 1], weights=[0.9, 0.1])[0])
        self.breakable = bool(random.choices([0, 1], weights=[0.6, 0.4])[0])
        self.breakable_steps = int(random.uniform(1, 3))

    def steping(self, rect):
        if self.breakable:
          if not self.breakable_steps:
            return False

        left_point = rect.x >= self.rect.x and rect.x <= self.rect.x + self.rect.w
        right_point = rect.x + rect.w >= self.rect.x and rect.x + rect.w <= self.rect.x + self.rect.w

        if left_point or right_point:
            if rect.y > self.rect.y and rect.y < self.rect.y + self.rect.h:
              if self.breakable:
                self.breakable_steps -= 1

              return True
        return False

    def move_tile(self, view_width):
      if self.moveable:
        if self.move_dir_left:
          self.rect.x -= self.move_speed
          if self.rect.x < self.starting_x - self.move_range or self.rect.x < 0:
            self.move_dir_left = False

        else:
          self.rect.x += self.move_speed
          if self.rect.x > self.starting_x + self.move_range or self.rect.x + self.rect.w > view_width:
            self.move_dir_left = True

    def draw(self, drawer):
      if self.breakable:
        if self.breakable_steps == 1:
          drawer.drawTex("tile_broken1", self.rect)
        elif self.breakable_steps == 2:
          drawer.drawTex("tile_broken2", self.rect)
        elif self.breakable_steps == 3:
          drawer.drawTex("tile_broken3", self.rect)

        if self.booster and self.breakable_steps:
          drawer.drawTex("booster", self.rect)

        return

      if self.booster:
        drawer.drawTex("tile", self.rect)
        drawer.drawTex("booster", self.rect)
      else:
        drawer.drawTex("tile", self.rect)

class Game():
    drawer = Drawer()

    def __init__(self):
        self.level = 0
        self.level_best = 0

        self.view_levels = 15
        self.level_height = 70
    
        self.view_width = 500
        self.view_height = 700

        self.max_level_skips = 1
        self.camera_move = 0
        
        self.gravity = 0.1
        self.person = Person()
        self.floors = [ Floor(Rect(-100, -10, 700, 30)) ]
        self.time = time_ms()
    
        self.level_skips = 0
        self.finished = False

        for i in range(self.view_levels - 1):
          self.add_floor()

        self.person.x_pos = self.floors[0].rect.x
        self.person.rect.x = self.person.x_pos

        self.view_width = self.drawer.size[0]

        if os.path.exists('score.txt'):
            with open('score.txt', 'r') as f:
              self.level_best = int(f.read())
        else:
            with open('score.txt', 'w') as f:
              f.write(str(0))

        self.floors[0].breakable = False
        self.floors[0].booster = False

    def add_floor(self):
        last = self.floors[-1]

        prob = 0.8
        max_level_skips = self.max_level_skips
        if last.booster:
          max_level_skips += 4
          prob = 0.1

        rand = random.choices([0, 1], weights=[1 - prob, prob])[0]

        if max_level_skips == self.level_skips or rand:
          ypos = last.rect.y + (self.level_skips + 1) * self.level_height
          rec = Rect((self.view_width - 200) * random.random(), ypos, 70, 20)
          self.floors.append(Floor(rec))
          self.level_skips = 0

        else:
          self.level_skips += 1

    def proc(self):

        # game over test
        if self.person.rect.y < -500:
          if not self.finished:
            with open('score.txt', 'w') as f:
              f.write(str(self.level_best))


          self.finished = True
          return

        if self.level_best < self.level:
          self.level_best = self.level

        # full wraping test
        if self.person.rect.x > self.view_width:
          self.person.rect.x -= self.view_width
        elif self.person.rect.x + self.person.rect.w < 0:
          self.person.rect.x += self.view_width

        # apply gravity
        self.person.y_vel -= self.gravity
        self.person.x_vel += -0.3 if self.person.x_vel > 0 else 0.3

        # move tiles
        for floor in self.floors:
          floor.move_tile(self.view_width)

        # proc intersections
        if self.person.y_vel < 0:
          for idx, floor in enumerate(self.floors):
              hit = floor.steping(self.person.rect)
              
              # wraping
              if not hit:
                  if self.person.rect.x + self.person.rect.w > self.view_width:
                    wraped_rec = self.person.rect
                    wraped_rec.x -= self.view_width
                    hit = floor.steping(wraped_rec)
                  elif self.person.rect.x < 0:
                    wraped_rec = self.person.rect
                    wraped_rec.x += self.view_width
                    hit = floor.steping(wraped_rec)

              if hit:
                  if floor.booster:
                    self.person.y_vel = self.person.y_vel_max * 1.5
                  else:
                    self.person.y_vel = self.person.y_vel_max

                  if idx != 0:
                    self.level += idx
                    self.camera_move = self.person.rect.y - 50

                  break

        # apply velocity
        self.person.rect.y += self.person.y_vel
        self.person.rect.x += self.person.x_vel


        # offset all elements
        if self.camera_move > 0:
          delta = self.camera_move / 30

          for floor in self.floors:
            floor.rect.y -= delta

          self.person.rect.y -= delta

          self.camera_move -= delta

        # remove unused floors
        for floor in self.floors:
          if floor.rect.y + floor.rect.h < 0:
            self.floors.remove(floor)
                
        # add floors
        if self.floors[-1].rect.y + self.level_height * self.level_skips < self.view_height: 
          self.add_floor()

    def draw(self):
        self.drawer.startDraw()

        # game over test
        if self.finished:
          self.drawer.drawText("Game Over Looser!", (100, 200))
          self.drawer.drawText("Score : " + str(self.level), (100, 240))
          self.drawer.drawText("Best : " + str(self.level_best), (100, 280))

          self.drawer.endDraw()
          return


        person_rec = Rect(self.person.rect.x, self.person.rect.y, self.person.rect.w, self.person.rect.h)
        if self.person.y_vel > 0:
          factor = self.person.y_vel / 20
          person_rec.h *= 1 + factor
          person_rec.w -= factor * 20

        self.drawer.drawTex("person", person_rec)

        # wraping
        if self.person.rect.x + self.person.rect.w > self.view_width:
          wraped_rec = person_rec
          wraped_rec.x -= self.view_width
          self.drawer.drawTex("person", wraped_rec)

        elif self.person.rect.x < 0:
          wraped_rec = person_rec
          wraped_rec.x += self.view_width
          self.drawer.drawTex("person", wraped_rec)


        for floor in self.floors:
          floor.draw(self.drawer)

        self.drawer.drawText("Score : " + str(self.level), (0, 0))
        self.drawer.drawText("Best : " + str(self.level_best), (0, 30))

        self.drawer.endDraw()

    def proc_drag_event(self, delta):
        self.person.x_vel += delta / 6
        if self.person.x_vel > self.person.x_vel_max:
          self.person.x_vel = self.person.x_vel_max
        elif self.person.x_vel < -self.person.x_vel_max:
          self.person.x_vel = -self.person.x_vel_max

game = Game()

# Run the game loop
running = True
mouse_pos = (0, 0)
mouse_down = False
mouse_delta = (0, 0)

while running:
    mouse_delta = (0, 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:
                mouse_delta = (event.pos[0] - mouse_pos[0], event.pos[1] - mouse_pos[1])
                mouse_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_down = True
                mouse_pos = event.pos
                mouse_delta = (0, 0)
            
            if game.finished:
              game = Game()

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
              mouse_down = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        game.proc_drag_event(-5)
    if keys[pygame.K_RIGHT]:
        game.proc_drag_event(5)

    game.proc_drag_event(mouse_delta[0])

    time.sleep(0.01)
    game.proc()
    game.draw()
