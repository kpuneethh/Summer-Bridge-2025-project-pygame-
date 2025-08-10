import pygame
from settings import *
import random

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.vel_y = random.choice([-3, 3])
        self.vel_x = random.choice([-3,3])
        self.original_y = y
        self.original_x = x
        self.stationary = False

    def update(self):
        if self.rect.y > (self.original_y + 100):
            self.vel_y = -3
        if self.rect.y < (self.original_y - 100):
            self.vel_y = 3

        if self.rect.x > (self.original_x + 100):
            self.vel_x = -3
        if self.rect.x < (self.original_x - 100):
            self.vel_x = 3

        
        self.rect.y += self.vel_y
        self.rect.x += self.vel_x
        
    def draw(self, screen, camera, color):
        pygame.draw.rect(screen, color, camera.apply(self.rect))