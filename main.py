import pygame
from player import Player
from enemy import Enemy
from boss import Boss
from platforms import Platform
from collectibles import Collectible
from settings import *
import random
import time
from camera import Camera
from Jungle_Asset_Pack import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Platform Game")
    
    clock = pygame.time.Clock()
    
    player = Player()

    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

    platforms = []
    start_platform = Platform(0, 100, 300, 30)
    start_platform.stationary = True
    
    collectible_list = []

    star_count = 0

    for i in range(1, 8):
        x = i * 500
        randy = random.randint(200, SCREEN_HEIGHT - 200)
        randwidth = random.randint(100, 200)
        collectible_list.append(Collectible(x + (randwidth / 2), randy - 50))
        platforms.append(Platform(x, randy, randwidth, 30))
    platforms.append(start_platform)

    enemies = []
    for i in range(5):
        rand = random.choice([True, False])
        randx = random.randint(800, WORLD_WIDTH - 100)
        enemies.append(Enemy(randx, 50, rand))

    boss = Boss()

    SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_ENEMY_EVENT, 5000) 

    scroll = 0

    ground_image = pygame.image.load("Jungle_Asset_Pack/ground.png").convert_alpha()
    ground_width = ground_image.get_width()
    ground_height = ground_image.get_height()

    bg_images = []
    for i in range(1, 6):
        bg_image = pygame.image.load(f"Jungle_Asset_Pack/parallax_bg/plx-{i}.png").convert_alpha()
        bg_images.append(bg_image)
    bg_width = bg_images[0].get_width()

    def draw_bg():
        for i, img in enumerate(bg_images):
            speed = 1 + i * 0.2 # adjusts speed for each layer
            bg_width = img.get_width()

            x_pos = int(- (camera.offset.x * speed) % bg_width)

            screen.blit(img, (x_pos - bg_width, 0))
            screen.blit(img, (x_pos, 0))


    def draw_ground():
        speed = 2.5
        gw = ground_width
        y = SCREEN_HEIGHT - ground_height

        start_x = int(-camera.offset.x * speed) % gw - gw

        x = start_x
        while x < SCREEN_WIDTH:
            screen.blit(ground_image, (x, y))
            x += gw



    running = True

    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update(platforms, enemies, boss)
        camera.update(player)

        screen.fill(BLACK)

        draw_bg()
        draw_ground()
        for platform in platforms:
            platform.draw(screen, camera, WHITE)
            if platform.stationary == False:
                platform.update() 

        for collectible in collectible_list:
            if player.rect.colliderect(collectible.rect):
                collectible.claimed = True
            if collectible.claimed == False:
                collectible.draw(screen,camera)
        
        for i in range(len(collectible_list)):
            if collectible_list[i].claimed == False:
                break
            if i == (len(collectible_list) - 1) and collectible_list[i].claimed == True:
                player.won = True
                running = False


        start_platform.draw(screen, camera, YELLOW)
        player.draw(screen, camera)
        for enemy in enemies:
            enemy.draw(screen, camera)
            enemy.update(platforms)

        boss.draw(screen, camera)
        boss.update(platforms, player)
        
        pygame.display.flip()
        clock.tick(FPS)

        if not player.alive:
            running = False

    if not player.alive:
            font = pygame.font.SysFont(None, 72)
            screen.fill(RED)
            game_over = font.render("YOU'VE BEEN EATEN!", True, WHITE)
            game_over_text_box = game_over.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(game_over, game_over_text_box)
            pygame.display.flip()
            pygame.time.wait(2000)
    elif player.won:
            font = pygame.font.SysFont(None, 72)
            screen.fill(GREEN)
            game_over = font.render("YOU MADE IT!", True, WHITE)
            game_over_text_box = game_over.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(game_over, game_over_text_box)
            pygame.display.flip()
            pygame.time.wait(2000)
    else:
            font = pygame.font.SysFont(None, 72)
            screen.fill(RED)
            game_over = font.render("COWARDLY!", True, WHITE)
            game_over_text_box = game_over.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(game_over, game_over_text_box)
            pygame.display.flip()
            pygame.time.wait(1000)

    pygame.quit()

if __name__ == "__main__":
    main()  
