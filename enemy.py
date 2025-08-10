import pygame
from settings import *
import random

class Enemy:
    def __init__(self, x, y, rand):
        self.image = pygame.image.load("harrel.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center = (x, y))

        #self.rect = pygame.Rect(x, y, 50, 50)
        self.vel_y = 0
        self.vel_x = 0
        self.on_ground = False
        self.walk_left = rand

    def update(self, platforms):
        if self.walk_left == True:
            self.vel_x = -6
            self.rect.x += self.vel_x
            if self.rect.left < 0:
                self.rect.left = 0
                self.walk_left = False
        else:
            self.vel_x = 6
            self.rect.x += self.vel_x
            if self.rect.right > WORLD_WIDTH:
                self.rect.right = WORLD_WIDTH
                self.walk_left = True

        self.rect.x += self.vel_x

        # horizontal collisions
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_x > 0:
                    self.rect.right = platform.rect.left
                    self.walk_left = True
                elif self.vel_x < 0:
                    self.rect.left = platform.rect.right
                    self.walk_left = False

        self.vel_y += 2
        self.rect.y += self.vel_y

        
        self.on_ground = False

        # platform landing
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Falling down
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True

        if self.rect.bottom >= SCREEN_HEIGHT - 60:
            self.rect.bottom = SCREEN_HEIGHT - 60
            self.vel_y = 0
            self.on_ground = True


    def draw(self, surface, camera):
        surface.blit(self.image, camera.apply(self.rect))