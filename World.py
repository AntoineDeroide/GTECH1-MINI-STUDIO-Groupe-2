import pygame
import time
from pygame.locals import *

pygame.init()

screen_width = 1000
screen_height = 700
tile_size = 50
move_speed = 8

clock = pygame.time.Clock()
fps = 60
dt = 0


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

bg_img = pygame.image.load("sky-blue-color-solid-background-1920x1080.png").convert()

class World:
    def __init__(self, data):
        self.tile_list = []
        dirt_img = pygame.image.load("dirt.png").convert_alpha()
        grass_img = pygame.image.load("grass.png").convert_alpha()

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    self.tile_list.append((img, img_rect))
                elif tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    self.tile_list.append((img, img_rect))
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

class Player:
    def __init__(self, x, y):
        img = pygame.image.load("tile_0000.png").convert_alpha()
        self.image = pygame.transform.scale(img, (56, 56))
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.on_ground = False
        self.jump_power = 15
        self.gravity = 1.25
        self.dash_power = 40
        self.dash_speed = 0
        self.dash_acceleration = 5
        self.dash_duration = 0.1  # Durée du dash en secondes
        self.dash_timer = 0
        self.allow_dash = True

    def update(self):
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()
        if key[K_q]:
            dx -= move_speed
            self.dash_direction = -1
        if key[K_d]:
            dx += move_speed
            self.dash_direction = 1

        # Jump
        if key[K_SPACE] and self.on_ground:
            self.vel_y = -self.jump_power
            self.on_ground = False

        # Dash
        if key[K_LSHIFT] and self.dash_timer <= 0 and self.allow_dash and not self.on_ground:
            self.dash_speed += self.dash_acceleration
            if self.dash_speed >= self.dash_power:
                self.dash_speed = self.dash_power
                self.dash_timer = self.dash_duration
                self.allow_dash = False
            # Mettre à jour la position du joueur en fonction de la vitesse de dash et de la direction
            self.rect.x += self.dash_speed * self.dash_direction
            self.vel_y = 0
        elif self.dash_timer > 0:
            self.dash_timer -= dt
            self.dash_speed = 0
        elif self.on_ground:
            self.allow_dash = True


        # Apply gravity
        self.vel_y += self.gravity
        if self.vel_y > 10:
            self.vel_y = 10

        dy += self.vel_y

        # Check collisions
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0

            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                    self.dash = False
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.on_ground = True

        # Update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        screen.blit(self.image, self.rect)

world_data = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 1, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1, 1, 0, 0, 1, 1],
[0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

world = World(world_data)
player = Player(100, screen_height - 130)

run = True
while run:
    start = pygame.time.get_ticks() 
    screen.blit(bg_img, (0, 0))

    world.draw()
    player.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    targetTime = 1000 / fps
    if dt < targetTime:
        pygame.time.delay(int(targetTime - dt))
    dt = pygame.time.get_ticks() - start
    dt /= 1000 

    pygame.display.update()

pygame.quit()