from games import GamesProtocol
import pygame
import time
from shapes import GameDisplay, FrameRate
from typing import List, Tuple, Optional
from game_handler import GameHandler

class SelectionScreen:
    def __init__(self, games: List[type[GamesProtocol]]):
        # Set up the drawing window
        SCREEN_W = 500
        SCREEN_H = 500

        self.games = games
        self.idx_to_name = {i : game.game_name() for i, game in enumerate(games)}

        self.screen = pygame.display.set_mode([SCREEN_W, SCREEN_H])

        num_games = len(games)
        num_colums = 3
        num_rows = num_games // num_colums + bool(num_games % 3)
        x_options = [SCREEN_W / (num_colums + 1) * (i + 1) for i in range(num_colums)]
        y_options = [SCREEN_H / (num_rows + 1)* (i + 1) for i in range(num_rows)]

        self.game_displays : List[GameDisplay] = []

        game_slots: List[Tuple[float,float]] = []
        for y_option in y_options:
            for x_option in x_options:
                game_slots.append((x_option, y_option))

        for idx, game in enumerate(games):
            self.game_displays.append(GameDisplay(f"{idx}: {game.game_name()}", game_slots[idx][0], game_slots[idx][1]))

        self.frame_rate = FrameRate(SCREEN_W//16, SCREEN_H//16)

        rate = 60
        self.dt = 1 / rate

    def return_game_idx(self) -> Optional[int]:
        if pygame.key.get_pressed()[pygame.K_0]:
            return 0
        if pygame.key.get_pressed()[pygame.K_1]:
            return 1
        if pygame.key.get_pressed()[pygame.K_2]:
            return 2
        if pygame.key.get_pressed()[pygame.K_3]:
            return 3
        if pygame.key.get_pressed()[pygame.K_4]:
            return 4
        if pygame.key.get_pressed()[pygame.K_5]:
            return 5
        if pygame.key.get_pressed()[pygame.K_6]:
            return 6
        if pygame.key.get_pressed()[pygame.K_7]:
            return 7
        if pygame.key.get_pressed()[pygame.K_8]:
            return 8
        if pygame.key.get_pressed()[pygame.K_9]:
            return 9
    

    def loop(self) -> bool:
        start = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
        game_idx = self.return_game_idx()
        if game_idx is not None and game_idx < len(self.games):
            print("Here")
            game_handler =  GameHandler(self.games[game_idx])

            game_running = True
            while game_running:
                game_running = game_handler.loop()


        # Fill the background with white
        self.screen.fill((255, 255, 255))

        for display in self.game_displays:
            display.update(self.dt)
            display.get_collider().draw(self.screen)

        loop_time = time.time() - start

        if self.dt - loop_time > 0:
            time.sleep(self.dt - loop_time)

        self.frame_rate.set_frame_rate(1/(time.time()-start))
        self.frame_rate.get_collider().draw(self.screen)
        pygame.display.flip()

        return True