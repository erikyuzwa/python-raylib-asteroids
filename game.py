import pyray as pr
from resource_type import ResourceType
from entity import Entity
import math
import numpy as np
from copy import copy

MAX_METEORS = 30
MAX_SHOTS = 5

class Game:
  def __init__(self, screenWidth, screenHeight):
    self.resources = {}
    self.meteors = []
    self.shots = []
    self.player = Entity()
    self.screenWidth = screenWidth
    self.screenHeight = screenHeight

  def startup(self):
    pr.init_audio_device()

    image1 = pr.load_image("assets/meteor_small.png")
    self.resources[ResourceType.TEXTURE_METEOR_SMALL] = pr.load_texture_from_image(image1)
    pr.unload_image(image1)

    image1 = pr.load_image("assets/meteor_med.png")
    self.resources[ResourceType.TEXTURE_METEOR_MED] = pr.load_texture_from_image(image1)
    pr.unload_image(image1)

    image1 = pr.load_image("assets/meteor_large.png")
    self.resources[ResourceType.TEXTURE_METEOR_LARGE] = pr.load_texture_from_image(image1)
    pr.unload_image(image1)

    image1 = pr.load_image("assets/player.png")
    self.resources[ResourceType.TEXTURE_PLAYER] = pr.load_texture_from_image(image1)
    pr.unload_image(image1)

    self.resources[ResourceType.SOUND_LASER_SHOOT] = pr.load_sound("assets/laser-shoot.wav")
    self.resources[ResourceType.SOUND_LASER_EXPLOSION] = pr.load_sound("assets/laser-explosion.wav")

    self.reset()

  def update(self):
    if pr.is_key_down(pr.KEY_LEFT):
      self.player.heading -= 5.0
    elif pr.is_key_down(pr.KEY_RIGHT):
      self.player.heading += 5.0
    elif pr.is_key_down(pr.KEY_UP):
      if self.player.acceleration < 1.0:
        self.player.acceleration += 0.04

    if pr.is_key_pressed(pr.KEY_LEFT_CONTROL):
      shot = Entity()
      shot.active = True
      shot.position.x = copy(self.player.position.x)
      shot.position.y = copy(self.player.position.y)
      shot.heading = copy(self.player.heading)
      shot.acceleration = 1.0
      shot.speed.x = math.cos(np.deg2rad(self.player.heading)) * 10.0
      shot.speed.y = math.sin(np.deg2rad(self.player.heading)) * 10.0
      self.shots.append(shot)
      pr.play_sound(self.resources[ResourceType.SOUND_LASER_SHOOT])

    # player speed
    self.player.speed.x = math.cos(np.deg2rad(self.player.heading)) * 6.0
    self.player.speed.y = math.sin(np.deg2rad(self.player.heading)) * 6.0

    self.player.position.x += (self.player.speed.x * self.player.acceleration)
    self.player.position.y += (self.player.speed.y * self.player.acceleration)

    if self.player.position.x > self.screenWidth:
      self.player.position.x = 0.0
    elif self.player.position.x < 0.0:
      self.player.position.x = self.screenWidth
      
    if self.player.position.y > self.screenHeight:
      self.player.position.y = 0.0
    elif self.player.position.y < 0.0:
      self.player.position.y = self.screenHeight
    
    for meteor in self.meteors:
      if meteor.active == True:
        meteor.position.x += meteor.speed.x * math.cos(np.deg2rad(meteor.heading))
        meteor.position.y += meteor.speed.y * math.sin(np.deg2rad(meteor.heading))
        if meteor.position.x > self.screenWidth:
          meteor.position.x = 0.0
        elif meteor.position.x < 0.0:
          meteor.position.x = self.screenWidth

        if meteor.position.y > self.screenHeight:
          meteor.position.y = 0.0
        elif meteor.position.y < 0.0:
          meteor.position.y = self.screenHeight

    for shot in self.shots:
      if shot.active == True:
        shot.position.x += (shot.speed.x * shot.acceleration)
        shot.position.y += (shot.speed.y * shot.acceleration)
        if shot.position.x > self.screenWidth or shot.position.x < 0:
          shot.active = False
        if shot.position.y > self.screenHeight or shot.position.y < 0:
          shot.active = False

    for shot in self.shots:
      if shot.active == True:
        for meteor in self.meteors:
          if meteor.active == True:
            texture = ResourceType(meteor.type)
            if pr.check_collision_circles(shot.position, 1, meteor.position, self.resources[texture].width // 2) == True:
              # collision!
              meteor.active = False
              shot.active = False
              pr.play_sound(self.resources[ResourceType.SOUND_LASER_EXPLOSION])
              break

    active_shots = filter(lambda x: (x.active == True), self.shots)
    self.shots = list(active_shots)

    active_meteors = filter(lambda x: (x.active == True), self.meteors)
    self.meteors = list(active_meteors)

    # print("meteor list size: " + str(len(self.meteors)))

    

  def render(self):
    for meteor in self.meteors:
      texture = ResourceType(meteor.type)
      pr.draw_texture_pro(
        self.resources[texture],
        pr.Rectangle(
          0, 0, self.resources[texture].width, self.resources[texture].height
        ),
        pr.Rectangle(
          meteor.position.x, meteor.position.y, self.resources[texture].width, self.resources[texture].height
        ),
        pr.Vector2(self.resources[texture].width // 2, self.resources[texture].height // 2),
        meteor.heading,
        pr.WHITE
      )

    for shot in self.shots:
      pr.draw_circle(int(shot.position.x), int(shot.position.y), 1.0, pr.YELLOW)

    pr.draw_texture_pro(
      self.resources[ResourceType.TEXTURE_PLAYER],
      pr.Rectangle(0, 0, self.resources[ResourceType.TEXTURE_PLAYER].width, self.resources[ResourceType.TEXTURE_PLAYER].height),
      pr.Rectangle(self.player.position.x, self.player.position.y, self.resources[ResourceType.TEXTURE_PLAYER].width // 2, self.resources[ResourceType.TEXTURE_PLAYER].height // 2),
      pr.Vector2(self.resources[ResourceType.TEXTURE_PLAYER].width // 4, self.resources[ResourceType.TEXTURE_PLAYER].height // 4),
      self.player.heading,
      pr.WHITE
    )

  def shutdown(self):
    pr.unload_texture(self.resources[ResourceType.TEXTURE_METEOR_SMALL])
    pr.unload_texture(self.resources[ResourceType.TEXTURE_METEOR_MED])
    pr.unload_texture(self.resources[ResourceType.TEXTURE_METEOR_LARGE])
    pr.unload_texture(self.resources[ResourceType.TEXTURE_PLAYER])

    pr.unload_sound(self.resources[ResourceType.SOUND_LASER_SHOOT])
    pr.unload_sound(self.resources[ResourceType.SOUND_LASER_EXPLOSION])

  pr.close_audio_device()

  def reset(self):
    self.player.position = pr.Vector2(self.screenWidth // 2, self.screenHeight // 2)
    self.player.speed = pr.Vector2(0, 0)
    self.player.heading = 0.00
    self.player.acceleration = 0.00
    self.player.active = True

    self.shots.clear()
    self.meteors.clear()

    for i in range(MAX_METEORS):
      meteor = Entity()
      meteor.active = True
      meteor.heading = float(pr.get_random_value(0, 360))
      meteor.position = pr.Vector2(
        float(pr.get_random_value(0, self.screenWidth)),
        float(pr.get_random_value(0, self.screenHeight))
      )
      meteor.type = pr.get_random_value(ResourceType.TEXTURE_METEOR_SMALL.value, ResourceType.TEXTURE_METEOR_LARGE.value)
      meteor.speed = pr.Vector2(
        float(pr.get_random_value(1, 2)),
        float(pr.get_random_value(1, 2))
      )
      self.meteors.append(meteor)
