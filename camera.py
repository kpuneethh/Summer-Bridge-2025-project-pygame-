import pygame
from settings import WORLD_WIDTH, SCREEN_HEIGHT

class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.offset = pygame.Vector2(0, 0)  
        self.camera_rect = pygame.Rect(0, 0, width, height)

    def apply(self, target_rect):
        return target_rect.move(-self.offset.x, -self.offset.y)

    def update(self, target):
        desired_x = target.rect.centerx - self.width // 2
        desired_y = target.rect.centery - self.height // 2

        desired_x = max(0, min(desired_x, WORLD_WIDTH - self.width))
        desired_y = max(0, min(desired_y, SCREEN_HEIGHT - self.height))

        # used for smooth following
        self.offset.x += (desired_x - self.offset.x) * 0.1
        self.offset.y += (desired_y - self.offset.y) * 0.1

        self.camera_rect.topleft = (int(self.offset.x), int(self.offset.y))

