import pyray as pr
import game

screenWidth = 1280
screenHeight = 720

current_game = game.Game(screenWidth, screenHeight)

if __name__ == '__main__':  

  pr.init_window(screenWidth, screenHeight, "Python Asteroids")
  pr.set_target_fps(60)

  current_game.startup()

  while not pr.window_should_close():

    current_game.update()
      
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)

    current_game.render()

    pr.end_drawing()

  pr.close_window()
  
  current_game.shutdown()
