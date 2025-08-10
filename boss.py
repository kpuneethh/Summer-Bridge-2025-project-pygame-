import pygame
from settings import *
import random

class Boss:
    def __init__(self):
        self.image = pygame.image.load("monster.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect(center = (WORLD_WIDTH - 200, 400))

        self.vel_y = 0
        self.vel_x = 0
        self.on_ground = False
        self.walk_left = True

    def update(self, platforms, player):
        if self.walk_left == True:
            self.rect.x -= 4
            if self.rect.left < 0:
                self.rect.left = 0
                self.walk_left = False
        else:
            self.rect.x += 4
            if self.rect.right > WORLD_WIDTH:
                self.rect.right = WORLD_WIDTH
                self.walk_left = True


        self.vel_y += 2
        self.rect.y += self.vel_y

        # collisions

        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Falling down
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_x > 0:
                    self.rect.right = platform.rect.left
                    self.walk_left = True
                elif self.vel_x < 0:
                    self.rect.left = platform.rect.right
                    self.walk_left = False

        if self.rect.bottom >= SCREEN_HEIGHT - 60:
            self.rect.bottom = SCREEN_HEIGHT - 60
            self.vel_y = 0
            self.on_ground = True

        if player.rect.x > self.rect.x:
            if abs(player.rect.x - self.rect.x) > 300:
                self.walk_left = False
        else:
            if abs(player.rect.x - self.rect.x) > 300:
                self.walk_left = True
        if abs(player.rect.x - self.rect.x) < 300 and self.on_ground and self.rect.y - player.rect.y > 100:
            self.vel_y = -25

    def draw(self, surface, camera):
        surface.blit(self.image, camera.apply(self.rect))