import pygame
import time
from pygame.locals import *
import pickle

pygame.init()

screen_width = 1000
screen_height = 700
tile_size = 50
move_speed = 10
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1
level = 0


clock = pygame.time.Clock()
fps = 60
dt = 0

res = "img/mouvement/hidl/animation stand1.png"
animations_walk = ["img/mouvement/run/course1.png", "img/mouvement/run/course2.png", "img/mouvement/run/course3.png"]
animations_standing = ["img/mouvement/hidl/animation stand1.png", "img/mouvement/hidl/animation stand2.png", "img/mouvement/hidl/animation stand3.png", "img/mouvement/hidl/animation stand4.png", "img/mouvement/hidl/animation stand5.png"]
animations_air_jump = ["img/mouvement/double jump/double jump1.png", "img/mouvement/double jump/double jump2.png", "img/mouvement/double jump/double jump3.png", "img/mouvement/double jump/double jump4.png"]
animations_jump = ["img/mouvement/run jump/run_jump1.png", "img/mouvement/run jump/run_jump2.png", "img/mouvement/run jump/run_jump3.png", "img/mouvement/run jump/run_jump4.png"]
animations_monte = ["img/mouvement/run jump/run_jump5.png", "img/mouvement/run jump/run_jump6.png"]
animations_falling = ["img/mouvement/run jump/run_jump7.png", "img/mouvement/run jump/run_jump8.png"]
animations_landing = ["img/mouvement/run jump/run_jump9.png", "img/mouvement/run jump/run_jump10.png"]
animations_dash = ["img/mouvement/dash/dash1.png", "img/mouvement/dash/dash2.png",]
animations_start_slide = ["img/mouvement/slide/slide1.png"]
animations_slide = ["img/mouvement/slide/slide2.png", "img/mouvement/slide/slide3.png"]
# annimation_degats = ["img/mouvement/degat/"]



#define colours
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

pine1_img = pygame.image.load('img/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/sky_cloud.png').convert_alpha()

def draw_bg():
	screen.fill(GREEN)
	width = sky_img.get_width()
	for x in range(4):
		screen.blit(sky_img, ((x * width) - scroll * 0.5, 0))
		screen.blit(mountain_img, ((x * width) - scroll * 0.6, screen_height - mountain_img.get_height() - 300))
		screen.blit(pine1_img, ((x * width) - scroll * 0.7, screen_height - pine1_img.get_height() - 150))
		screen.blit(pine2_img, ((x * width) - scroll * 0.8, screen_height - pine2_img.get_height()))

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(screen_width / 2)
        y = -target.rect.centery + int(screen_height / 2)

        # limit scrolling to map size
        x = min(0, x)  
        y = min(0, y)  
        x = max(-(self.width - screen_width), x) 
        y = max(-(self.height - screen_height), y) 

        self.camera = pygame.Rect(x, y, self.width, self.height)

class World:
    def __init__(self, data):
        self.tile_list = []

        if not data:
            self.width = 0
            self.height = 0
            return 

        self.width = len(data[0]) * tile_size
        self.height = len(data) * tile_size

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
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self, camera):
        for tile in self.tile_list: 
            screen.blit(tile[0], camera.apply(tile[1]))

class Player:
    def __init__(self, x, y):
        link_img = "img/mouvement/hidl/animation stand1.png"
        self.img = pygame.image.load(link_img).convert_alpha()
        self.image = pygame.transform.scale(self.img, (56, 56))
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = x
        self.rect.y = y

        self.walk_speed = 500 #vitesse de marche
        self.speed_multiplication = 1
        self.current_speed_x = 0
        self.current_speed_y = 0
        self.dir_x = 0
        self.dir_y = 0

        self.gravity = 1.2 #force de la gravité
        self.gravity_coefficient = 1 #acceleration de la gravité

        self.on_ground = False
        self.on_wall = False

        self.dash_power = 40 #puissance du dash
        self.dash_acceleration = 5 #accélération du dash
        self.dash_duration = 0.1 #durée du dash
        self.dash_speed = 0
        self.dash_timer = 0
        self.dash_direction = 0
        self.dash_allow = True

        self.jump_power = 17 #puissance du saut
        self.maxjump = 2 #nombre de sauts
        self.nbr_jump = 0
        self.space_pressed = False

        self.slide_speed = 4.0 #vitesse du slide (quoeficient d'acceleration de la vitesse)
        self.slide_duration = 0.3 #durée du slide
        self.is_sliding = False
        self.slide_timer = 0

        #listes des annimation
        self.annim_standing = 0
        self.annim_walk = 0
        self.annim_jump = 0
        self.annim_air_jump = 0
        self.annim_monte = 0
        self.annim_falling = 0
        self.annim_falling_landing = 0
        self.annim_dash = 0
        self.annim_start_slide = 0
        self.annim_slide = 0
        
        self.annim_timer = 0
        self.annim_timer_frame = 0.1
        self.nbr_frame = 0
        self.player_oritentation = 1
        self.x_size = 56

    def annimation(self):
        walk = False
        jump = False
        air_jump = False
        falling = False
        dash = False
        slide = False
        monte = False
        nbr_frame_slide = 2
        nbr_frame_saut = 4

        liste_var = [walk, jump, air_jump, monte, falling, dash, slide]
        liste_annim = [self.annim_walk, self.annim_jump, self.annim_air_jump, self.annim_monte, self.annim_falling, self.annim_dash, self.annim_slide]
        self.annim_timer -= dt
        if self.annim_timer <= 0:
            self.annim_timer = self.annim_timer_frame

            if self.dash_timer > 0 : #dash
                dash = True
                res = animations_dash[self.annim_dash]
                self.annim_dash = (self.annim_dash + 1) % (len(animations_dash))
                self.x_size = 56
            
            elif self.is_sliding:
                slide = True
                if self.nbr_frame <= nbr_frame_slide:
                    res = animations_start_slide[self.annim_start_slide]
                    self.annim_start_slide = (self.annim_start_slide + 1) % (len(animations_start_slide))
                    self.nbr_frame += 1
                    self.x_size = 60
                else:
                    res = animations_slide[self.annim_slide]
                    self.annim_slide = (self.annim_slide + 1) % (len(animations_slide))
                    self.x_size = 60

            elif self.space_pressed and self.on_ground and self.nbr_frame <= nbr_frame_saut: #saut
                jump = True
                res = animations_jump[self.annim_jump]
                self.annim_jump = (self.annim_jump + 1) % (len(animations_jump))
                self.nbr_frame += 1
                self.x_size = 56
            
            elif self.space_pressed and not self.on_ground and self.nbr_frame <= nbr_frame_saut: #2eme saut 
                air_jump = True
                res = animations_air_jump[self.annim_air_jump]
                self.annim_air_jump = (self.annim_air_jump + 1) % (len(animations_air_jump))
                self.nbr_frame += 1
                self.x_size = 56

            elif self.current_speed_y < 0 and not self.on_ground: #monté
                monte = True
                res = animations_monte[self.annim_monte]
                self.annim_monte = (self.annim_monte + 1) % (len(animations_monte))
                self.x_size = 56

            elif self.current_speed_y  > 5 : #chute
                res = animations_falling[self.annim_falling]
                self.annim_standing = (self.annim_standing + 1) % (len(animations_falling))
                falling = True
                self.x_size = 56
            
            elif (key[K_d] or key[K_q]) and self.on_ground: #walk 
                res = animations_walk[self.annim_walk]
                self.annim_walk = (self.annim_walk + 1) % (len(animations_walk))
                walk = True
                self.x_size = 90
            
            else:
                res = animations_standing[self.annim_standing]
                self.annim_standing = (self.annim_standing + 1) % (len(animations_standing))
                self.x_size = 56


            for i in liste_var:
                if not liste_var[i]:
                    liste_annim[i] = 0

            if not slide and not jump and not air_jump:
                self.nbr_frame = 0
                    
            self.refresh_img(res)
    
    def refresh_img(self, link):
        self.img = pygame.image.load(link).convert_alpha()
        self.image = pygame.transform.scale(self.img, (self.x_size, 56))

    def set_velocity_x(self, dir_x, speed):
        self.current_speed_x = dir_x * speed

    def set_velocity_y(self, dir_y, speed):
        self.current_speed_y = dir_y * speed

    def update(self):


        dx = self.current_speed_x * dt
        dy = self.current_speed_y * dt
        
    #gravity
        self.current_speed_y += self.gravity * self.gravity_coefficient ** dt
        dy += self.current_speed_y
    #end of gravity

    # Check collisions
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0

            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.current_speed_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.current_speed_y = 0
                elif self.current_speed_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.current_speed_y = 0
                    self.on_ground = True
                    self.nbr_jump = 0
    #end of collision check

    # Update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        if self.current_speed_x >= 0:
            self.player_oritentation = 1
            self.current_speed_x = max(0, self.current_speed_x - ( 2000 * dt  * self.speed_multiplication))
        else:
            self.current_speed_x = min(0, self.current_speed_x + ( 2000 * dt  * self.speed_multiplication))
            self.player_oritentation = -1
    #end of Update player coordinates

    def draw(self, camera):
        # Si player_orientation est 1, pas besoin de retourner l'image
        if self.player_oritentation == 1:
            screen.blit(self.image, camera.apply(self.rect))
        # Si player_orientation est -1, retourner l'image horizontalement
        elif self.player_oritentation == -1:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, camera.apply(self.rect))



file_path = 'map/2map.txt'

with open(file_path, 'r') as file:
    world_data = [list(map(int, line.strip().split(','))) for line in file]
world = World(world_data)
player = Player(100, screen_height - 130)
camera = Camera(world.width, world.height)

run = True
while run:
    start = pygame.time.get_ticks()

#movement
    key = pygame.key.get_pressed()
    if key[K_q] and (not player.is_sliding or abs(player.current_speed_x) <= 20):
        player.set_velocity_x(-1, player.walk_speed)
    if key[K_d] and (not player.is_sliding or abs(player.current_speed_x) <= 20):
        player.set_velocity_x(1, player.walk_speed)
#end of movement

#jump
    if key[K_SPACE] and not player.is_sliding:
        if player.on_ground or player.on_wall:
            player.set_velocity_y(-1, player.jump_power)
            player.on_ground = False
            player.nbr_jump += 1
        elif not player.space_pressed and player.nbr_jump < player.maxjump and not player.on_ground and not player.on_wall:
            player.nbr_jump += 1
            player.set_velocity_y(-1, player.jump_power)
        player.space_pressed = True
    else:
        player.space_pressed = False
#end of jump

# Dash
    if key[K_LCTRL] and player.dash_timer <= 0 and player.dash_allow and not player.on_ground and not player.space_pressed :
        # Détermination de la direction du dash
        player.dash_direction = 1 if key[K_d] else -1 if key[K_q] else 0

        player.dash_speed += player.dash_acceleration
        if player.dash_speed >= player.dash_power:
            player.dash_speed = player.dash_power
            player.dash_timer = player.dash_duration
            player.dash_allow = False
        player.rect.x += player.dash_speed * player.dash_direction
        player.current_speed_y = 0
    elif player.dash_timer > 0:
        player.dash_timer -= dt
        player.dash_speed = 0
    elif player.on_ground:
        player.dash_allow = True
#end of dash

#slide
    if key[K_LSHIFT]:
        player.speed_multiplication = 0.5
        if player.on_ground and player.slide_timer <= 0 and not player.is_sliding:
            player.current_speed_x *=  player.slide_speed
            player.is_sliding = True
    else:
        player.is_sliding = False
        player.speed_multiplication = 1
 #end of slide

    player.annimation()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        
    draw_bg()

    camera.update(player)
    world.draw(camera)
    player.update()
    player.draw(camera)

    pygame.display.update()

    targetTime = 1000 / fps
    if dt < targetTime:
        pygame.time.delay(int(targetTime - dt))
    dt = pygame.time.get_ticks() - start
    dt /= 1000 

pygame.quit()
