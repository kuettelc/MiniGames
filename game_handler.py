from games import GamesProtocol
import pygame
import time
from shapes import FrameRate

class GameHandler:
    def __init__(self, game: type[GamesProtocol]):
        # Set up the drawing window
        SCREEN_W = 500
        SCREEN_H = 500

        self.screen = pygame.display.set_mode([SCREEN_W, SCREEN_H])

        self.game = game(self.screen)
        self.frame_rate = FrameRate(SCREEN_W//16, SCREEN_H//16)

        rate = 60
        self.dt = 1 / rate

    def loop(self) -> bool:
        start = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        # Fill the background with white
        self.screen.fill((255, 255, 255))

        self.game.loop()

        for shape in self.game.get_scene_objects():
            shape.update(self.dt)
            shape.get_collider().draw(self.screen)

        loop_time = time.time() - start

        if self.dt - loop_time > 0:
            time.sleep(self.dt - loop_time)

        self.frame_rate.set_frame_rate(1/(time.time()-start))
        self.frame_rate.get_collider().draw(self.screen)
        pygame.display.flip()

        return True
