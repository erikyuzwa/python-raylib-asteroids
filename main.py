import pyray as pr
import enum
import math
import numpy as np
import entity
import copy


screenWidth = 1280
screenHeight = 720

MAX_METEORS = 30
MAX_SHOTS = 5

resources = {}

player = entity.Entity()
meteors = []
shots = []


class ResourceType(enum.Enum):
  TEXTURE_METEOR_SMALL = 1
  TEXTURE_METEOR_MED = 2
  TEXTURE_METEOR_LARGE = 3
  TEXTURE_PLAYER = 4
  SOUND_LASER_SHOOT = 5
  SOUND_LASER_EXPLOSION = 6



def game_startup():
  pr.init_audio_device()

  image1 = pr.load_image("assets/player.png")
  resources[ResourceType.TEXTURE_PLAYER] = pr.load_texture_from_image(image1)
  pr.unload_image(image1)

  image1 = pr.load_image("assets/meteor_small.png")
  resources[ResourceType.TEXTURE_METEOR_SMALL] = pr.load_texture_from_image(image1)
  pr.unload_image(image1)

  image1 = pr.load_image("assets/meteor_med.png")
  resources[ResourceType.TEXTURE_METEOR_MED] = pr.load_texture_from_image(image1)
  pr.unload_image(image1)

  image1 = pr.load_image("assets/meteor_large.png")
  resources[ResourceType.TEXTURE_METEOR_LARGE] = pr.load_texture_from_image(image1)
  pr.unload_image(image1)

  resources[ResourceType.SOUND_LASER_SHOOT] = pr.load_sound("assets/laser-shoot.wav")
  resources[ResourceType.SOUND_LASER_EXPLOSION] = pr.load_sound("assets/laser-explosion.wav")


  game_reset()

def game_update():
  if pr.is_key_down(pr.KEY_LEFT):
    player.heading -= 5.0
  elif pr.is_key_down(pr.KEY_RIGHT):
    player.heading += 5.0
  elif pr.is_key_down(pr.KEY_UP):
    if player.acceleration < 1.0:
      player.acceleration += 0.04

  if pr.is_key_pressed(pr.KEY_LEFT_CONTROL):
    shot = entity.Entity()
    shot.active = True
    shot.position.x = copy.copy(player.position.x)
    shot.position.y = copy.copy(player.position.y)
    shot.heading = copy.copy(player.heading)
    shot.acceleration = 1.0
    shot.speed.x = math.cos(np.deg2rad(player.heading)) * 10.0
    shot.speed.y = math.sin(np.deg2rad(player.heading)) * 10.0
    shots.append(shot)
    pr.play_sound(resources[ResourceType.SOUND_LASER_SHOOT])


  # player speed
  player.speed.x = math.cos(np.deg2rad(player.heading)) * 6.0
  player.speed.y = math.sin(np.deg2rad(player.heading)) * 6.0

  player.position.x += (player.speed.x * player.acceleration)
  player.position.y += (player.speed.y * player.acceleration)

  if player.position.x > screenWidth:
    player.position.x = 0.0
  elif player.position.x < 0.0:
    player.position.x = screenWidth
  
  if player.position.y > screenHeight:
    player.position.y = 0.0
  elif player.position.y < 0.0:
    player.position.y = screenHeight

  for meteor in meteors:
    meteor.position.x += meteor.speed.x * math.cos(np.deg2rad(meteor.heading))
    meteor.position.y += meteor.speed.y * math.sin(np.deg2rad(meteor.heading))
    if meteor.position.x > screenWidth:
      meteor.position.x = 0.0
    elif meteor.position.x < 0.0:
      meteor.position.x = screenWidth

    if meteor.position.y > screenHeight:
      meteor.position.y = 0.0
    elif meteor.position.y < 0.0:
      meteor.position.y = screenHeight

  for shot in shots:
    if shot.active == True:
      shot.position.x += (shot.speed.x * shot.acceleration)
      shot.position.y += (shot.speed.y * shot.acceleration)


def game_render():

  for meteor in meteors:
    texture = ResourceType(meteor.type)
    pr.draw_texture_pro(
      resources[texture],
      pr.Rectangle(
        0, 0, resources[texture].width, resources[texture].height
      ),
      pr.Rectangle(
        meteor.position.x, meteor.position.y, resources[texture].width, resources[texture].height
      ),
      pr.Vector2(resources[texture].width // 2, resources[texture].height // 2),
      meteor.heading,
      pr.WHITE
    )

  for shot in shots:
    if shot.active == True:
      pr.draw_circle(int(shot.position.x), int(shot.position.y), 1.0, pr.YELLOW)

  pr.draw_texture_pro(
    resources[ResourceType.TEXTURE_PLAYER],
    pr.Rectangle(0, 0, resources[ResourceType.TEXTURE_PLAYER].width, resources[ResourceType.TEXTURE_PLAYER].height),
    pr.Rectangle(player.position.x, player.position.y, resources[ResourceType.TEXTURE_PLAYER].width // 2, resources[ResourceType.TEXTURE_PLAYER].height // 2),
    pr.Vector2(resources[ResourceType.TEXTURE_PLAYER].width // 4, resources[ResourceType.TEXTURE_PLAYER].height // 4),
    player.heading,
    pr.WHITE
  )




def game_shutdown():

  pr.unload_texture(resources[ResourceType.TEXTURE_METEOR_SMALL])
  pr.unload_texture(resources[ResourceType.TEXTURE_METEOR_MED])
  pr.unload_texture(resources[ResourceType.TEXTURE_METEOR_LARGE])
  pr.unload_texture(resources[ResourceType.TEXTURE_METEOR_PLAYER])

  pr.unload_sound(resources[ResourceType.SOUND_LASER_SHOOT])
  pr.unload_sound(resources[ResourceType.SOUND_LASER_EXPLOSION])

  pr.close_audio_device()


def game_reset():
  player.position = pr.Vector2(screenWidth // 2, screenHeight // 2)
  player.speed = pr.Vector2(0, 0)
  player.heading = 0.00
  player.acceleration = 0.00
  player.active = True

  global shots
  shots = []

  for i in range(MAX_METEORS):
    meteor = entity.Entity()
    meteor.active = True
    meteor.heading = float(pr.get_random_value(0, 360))
    meteor.position = pr.Vector2(
      float(pr.get_random_value(0, screenWidth)),
      float(pr.get_random_value(0, screenHeight))
    )
    meteor.type = pr.get_random_value(ResourceType.TEXTURE_METEOR_SMALL.value, ResourceType.TEXTURE_METEOR_LARGE.value)
    meteor.speed = pr.Vector2(
      float(pr.get_random_value(1, 2)),
      float(pr.get_random_value(1, 2))
    )
    meteors.append(meteor)

if __name__ == '__main__':  

  pr.init_window(screenWidth, screenHeight, "Raylib Asteroids")
  pr.set_target_fps(60)

  game_startup()

  while not pr.window_should_close():

    game_update()
      
    pr.begin_drawing()
    pr.clear_background(pr.BLUE)

    game_render()

    pr.end_drawing()

  pr.close_window()
  game_shutdown