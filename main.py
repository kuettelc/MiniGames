import pygame
import time
from games import Pong
from game_handler import GameHandler
# Initialize Pygame
pygame.init()


game_handler = GameHandler(Pong)

# Main loop
running = True
while running:
    running = game_handler.loop()



# Done! Time to quit.
pygame.quit()
