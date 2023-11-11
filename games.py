from shapes import Rectangle, Circle, Padel, Ball, Wall, ScoreBoard
from protocol import MovingShapeProtocol
import pygame
from typing import List, Protocol

class GamesProtocol(Protocol):
    def __init__(self, screen: pygame.Surface):
        ...

    def loop(self):
        ...

    def get_scene_objects(self) -> List[MovingShapeProtocol]:
        ...

class Pong(GamesProtocol):
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.SCREEN_H = screen.get_height()
        self.SCREEN_W = screen.get_width()

        self.PADEL_W = 20
        self.PADEL_H = 100

        self.PADEL_START = (self.SCREEN_H-self.PADEL_H) // 2

        self.padel_1 = Padel(Rectangle(0,self.PADEL_START,self.PADEL_W,self.PADEL_H), pygame.K_UP, pygame.K_DOWN, pygame.key)
        self.padel_2 = Padel(Rectangle(self.SCREEN_W - self.PADEL_W, self.PADEL_START,self.PADEL_W, self.PADEL_H),pygame.K_w, pygame.K_s, pygame.key)

        BALL_R = 10
        self.ball = Ball(Circle(200,200,BALL_R), 100, 50)

        self.ceiling = Wall(Rectangle(0,0,self.SCREEN_W, 2))
        self.floor = Wall(Rectangle(0, self.SCREEN_H-2, self.SCREEN_W,2))

        self.left_exit = Wall(Rectangle(-BALL_R-2,0,2,self.SCREEN_H))
        self.right_exit = Wall(Rectangle(self.SCREEN_W+BALL_R, 0, 2, self.SCREEN_H))

        self.score_board_1 = ScoreBoard("Player A", self.SCREEN_W/8, self.SCREEN_H/8)
        self.score_board_2 = ScoreBoard("Player B", self.SCREEN_W - self.SCREEN_W/8, self.SCREEN_H/8)


    def get_scene_objects(self) -> List[MovingShapeProtocol]:
        return [self.padel_1,self.padel_2,self.ball,self.ceiling,self.floor, self.score_board_1, self.score_board_2]
    
    def loop(self):
        if self.ball.collides(self.padel_2):
            self.ball.x_dir = -1
            self.ball.increase_speed(1.1)

        if self.ball.collides(self.padel_1):
            self.ball.x_dir = 1
            self.ball.increase_speed(1.1)

        if self.ball.collides(self.ceiling):
            self.ball.y_dir = 1

        if self.ball.collides(self.floor):
            self.ball.y_dir = -1

        if self.ball.collides(self.left_exit):
            print("Padel 2 has scored")
            self.score_board_2.increase_score()
            self.ball.reset()

        if self.ball.collides(self.right_exit):
            print("Padel 1 has scored")
            self.score_board_1.increase_score()
            self.ball.reset()

        for padel in [self.padel_1, self.padel_2]:
            padel.constrain_to_wall(self.ceiling)
            padel.constrain_to_wall(self.floor)