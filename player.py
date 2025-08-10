import pygame
from settings import *
import os

class Player:
    def __init__(self):
        self.image = pygame.image.load("sandwich.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (140, 100))
        self.rect = self.image.get_rect(center = (50, 0))

        self.vel_x = 0
        self.vel_y = 0
        self.acceleration = 0.5
        self.friction = 0.3
        self.max_speed = 6
        self.on_ground = False
        self.alive = True
        self.won = False



    def update(self, platforms, enemies, boss):
        keys = pygame.key.get_pressed()

        # acceleration
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x -= self.acceleration * (0.5 if not self.on_ground else 1)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x += self.acceleration * (0.5 if not self.on_ground else 1)
        else:
            # friction
            if self.vel_x > 0:
                self.vel_x -= self.friction
                if self.vel_x < 0:
                    self.vel_x = 0
            elif self.vel_x < 0:
                self.vel_x += self.friction
                if self.vel_x > 0:
                    self.vel_x = 0

        # max speed
        self.vel_x = max(-self.max_speed, min(self.vel_x, self.max_speed))

    
        self.rect.x += self.vel_x


        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x = 0
        if self.rect.right > WORLD_WIDTH:
            self.rect.right = WORLD_WIDTH
            self.vel_x = 0


        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = -25
            self.on_ground = False
        


        self.vel_y += 1
        self.rect.y += self.vel_y


        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_ground = True


        if self.rect.bottom >= SCREEN_HEIGHT - 60:
            self.rect.bottom = SCREEN_HEIGHT - 60
            self.vel_y = 0
            self.on_ground = True


        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                if self.vel_y > 0:
                    enemies.remove(enemy)
                    self.vel_y -= 40
                else:
                    self.alive = False
        if self.rect.colliderect(boss.rect):
            if self.vel_y > 0 or self.rect.y < boss.rect.y:
                self.vel_y -= 20
            else:
                self.alive = False

    def draw(self, surface, camera):
        surface.blit(self.image, camera.apply(self.rect))
