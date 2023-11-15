from __future__ import annotations

from pygame import Surface, Vector2
from pygame.event import Event
from protocol import ConvexShapeProtocol, MovingShapeProtocol
from pygame.key import ScancodeWrapper
import pygame
import math


class Text(ConvexShapeProtocol):
    def __init__(self, text: str, font: pygame.font.Font,x: float,y: float) -> None:
        self.text = text
        self.font = font
        self.x = x
        self.y = y
       
    def draw(self, screen: Surface):
        self.text_surface = self.font.render(self.text, True, (0,0,0))
        screen.blit(self.text_surface, [self.x - self.text_surface.get_width()/2, self.y - self.text_surface.get_height()])

    def set_text(self, text: str):
        self.text = text

    def _polygon(self):
        b_l = [self.x, self.y + self.text_surface.get_height()]
        b_r = [self.x + self.text_surface.get_width(), self.y + self.text_surface.get_height()]
        t_l = [self.x,self.y]
        t_r = [self.x + self.text_surface.get_width(), self.y]

        return [t_l, t_r, b_r, b_l]

class GameDisplay(MovingShapeProtocol):
    def __init__(self, game_name: str, x: float, y: float) -> None:
        self.text = Text(game_name, pygame.font.SysFont("arial", 10), x, y)

    def update(self, dt: float):
        return
    
    def get_collider(self) -> ConvexShapeProtocol:
        return self.text
    


class ScoreBoard(MovingShapeProtocol):
    def __init__(self, generic_text: str, x, y) -> None:
        self.generic_text = generic_text

        self.text = Text(self.generic_text, pygame.font.SysFont("arial", 10), x, y)

        self.score: int = 0

    def update(self, dt: float):
        self.text.set_text(f"{self.generic_text}: {self.score}")

    def increase_score(self):
        self.score += 1
    
    def get_collider(self) -> ConvexShapeProtocol:
        return self.text

class FrameRate(MovingShapeProtocol):
    def __init__(self, x, y) -> None:
        self.frame_rate = str(0)

        self.text = Text(self.frame_rate, pygame.font.SysFont("arial", 10), x, y)

    def update(self, dt: float):
        self.text.set_text(self.frame_rate)

    def set_frame_rate(self, frame_rate: float):
        self.frame_rate = str(int(frame_rate))
        self.update(0)

    def get_collider(self) -> ConvexShapeProtocol:
        return self.text

class Rectangle(ConvexShapeProtocol):
    def __init__(self, x:float, y:float, width:float, height:float) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.polygon = self._polygon()
    
    def draw(self, screen: Surface):
        pygame.draw.rect(screen,(0,0,0),(self.x,self.y,self.width,self.height))

    def _polygon(self):
        b_l = [self.x, self.y + self.height]
        b_r = [self.x + self.width, self.y + self.height]
        t_l = [self.x,self.y]
        t_r = [self.x + self.width, self.y]

        return [t_l, t_r, b_r, b_l]
    

class Padel(MovingShapeProtocol):
    def __init__(self, rectangle: Rectangle, up_key:int, down_key:int, key_handler) -> None:
        self.up_key = up_key
        self.down_key = down_key
        self.key_handler = key_handler
        self.rectangle = rectangle

    def update(self, dt: float):
        if self.key_handler.get_pressed()[self.down_key]:
            self.rectangle.y += 200*dt
        if self.key_handler.get_pressed()[self.up_key]:
            self.rectangle.y -= 200*dt

    def collides(self, other: MovingShapeProtocol):
        return self.rectangle.collides(other.get_collider())

    def constrain_to_wall(self,wall: Wall):
        padel_is_below = (self.rectangle.y  + self.rectangle.height/2) > (wall.rectangle.y + wall.rectangle.height/2)
        
        if (wall.rectangle.y + wall.rectangle.height > self.rectangle.y) and padel_is_below:
            self.rectangle.y = wall.rectangle.y + wall.rectangle.height
        if (wall.rectangle.y < self.rectangle.y + self.rectangle.height) and not padel_is_below:
            self.rectangle.y = wall.rectangle.y - self.rectangle.height

    def get_collider(self) -> ConvexShapeProtocol:
        return self.rectangle
    
class Padel2D(MovingShapeProtocol):
    def __init__(self, rectangle: Rectangle, up_key:int, down_key:int, right_key: int, left_key: int, key_handler) -> None:
        self.up_key = up_key
        self.down_key = down_key
        self.left_key = left_key
        self.right_key = right_key
        self.key_handler = key_handler
        self.rectangle = rectangle

    def update(self, dt: float):
        if self.key_handler.get_pressed()[self.down_key]:
            self.rectangle.y += 200*dt
        if self.key_handler.get_pressed()[self.up_key]:
            self.rectangle.y -= 200*dt
        if self.key_handler.get_pressed()[self.right_key]:
            self.rectangle.x += 200*dt
        if self.key_handler.get_pressed()[self.left_key]:
            self.rectangle.x -= 200*dt

    def collides(self, other: MovingShapeProtocol):
        return self.rectangle.collides(other.get_collider())

    def constrain_to_wall(self,wall: Wall):
        padel_is_below = (self.rectangle.y  + self.rectangle.height/2) > (wall.rectangle.y + wall.rectangle.height/2)
        
        if (wall.rectangle.y + wall.rectangle.height > self.rectangle.y) and padel_is_below:
            self.rectangle.y = wall.rectangle.y + wall.rectangle.height
        if (wall.rectangle.y < self.rectangle.y + self.rectangle.height) and not padel_is_below:
            self.rectangle.y = wall.rectangle.y - self.rectangle.height

    def get_collider(self) -> ConvexShapeProtocol:
        return self.rectangle

class Wall(MovingShapeProtocol):
    def __init__(self, rectangle: Rectangle):
        self.rectangle = rectangle

    def update(self, dt: float):
        return
    
    def collides(self, other:  MovingShapeProtocol):
        return self.rectangle.collides(other.get_collider())

    def get_collider(self) -> ConvexShapeProtocol:
        return self.rectangle

class Circle(ConvexShapeProtocol):
    def __init__(self, x:float, y:float, radius:float) -> None:
        self.x = x 
        self.y = y
        self.radius = radius
        self.polygon = self._polygon()

    def draw(self, screen: Surface):
        pygame.draw.circle(screen,(0,0,0),(self.x,self.y), self.radius)

    def _polygon(self):
        res = 100
        dpi = 2*math.pi / res
        angle_space = [dpi*i for i in range(res)]

        xs = [self.radius*math.cos(angle) + self.x for angle in angle_space]
        ys = [self.radius*math.sin(angle) + self.y for angle in angle_space]

        return [[x,y] for x,y in zip(xs,ys)]
    
class Ball(MovingShapeProtocol):
    def __init__(self, circle: Circle, dx: float, dy: float):
        self.circle = circle
        self.dx = dx
        self.dy = dy
        self.x_dir = 1
        self.y_dir = 1
        self.original_x = circle.x
        self.original_y = circle.y
        self.original_dx = dx
        self.original_dy = dy

    def update(self, dt: float):
        self.circle.x += self.dx*dt*self.x_dir
        self.circle.y += self.dy*dt*self.y_dir

    def collides(self, other: MovingShapeProtocol):
        return self.circle.collides(other.get_collider())

    def get_collider(self) -> ConvexShapeProtocol:
        return self.circle
    
    def increase_speed(self, dv):
        self.dx *= dv
        self.dy *= dv
    
    def reset(self):
        self.circle.x = self.original_x
        self.circle.y = self.original_y
        self.dx = self.original_dx
        self.dy = self.original_dy
    
    


