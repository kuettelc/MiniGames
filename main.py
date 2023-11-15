import pygame
from games import Pong2D, Pong
from game_handler import GameHandler
from selection_screen import SelectionScreen
# Initialize Pygame
pygame.init()


selection_screen = SelectionScreen([Pong,Pong2D])

# Main loop
running = True
while running:
    running = selection_screen.loop()



# Done! Time to quit.
pygame.quit()
