import pygame
from settings import *

class Collectible:
    def __init__(self, x, y):
        self.image = pygame.image.load("star.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center = (x, y))
        self.claimed = False
        
    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))