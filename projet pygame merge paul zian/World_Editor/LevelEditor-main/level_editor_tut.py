import pygame
import button
import csv

pygame.init()

clock = pygame.time.Clock()
FPS = 60

#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Editor')


#define game variables
ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 172
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1



#load images
pine1_img = pygame.image.load('World_Editor/LevelEditor-main/img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('World_Editor/LevelEditor-main/img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('World_Editor/LevelEditor-main/img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('World_Editor/LevelEditor-main/img/Background/sky_cloud.png').convert_alpha()
#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'World_Editor/LevelEditor-main/img/Cutted/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

save_img = pygame.image.load('World_Editor/LevelEditor-main/img/save_btn.png').convert_alpha()
load_img = pygame.image.load('World_Editor/LevelEditor-main/img/load_btn.png').convert_alpha()

tiles_per_page = 21
current_page = 0
total_pages = (TILE_TYPES + tiles_per_page - 1) // tiles_per_page

#define colours
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

#define font
font = pygame.font.SysFont('Futura', 30)

highlighted_button = None 
#create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)

#create ground
for tile in range(0, MAX_COLS):
    world_data[ROWS - 1][tile] = 0


#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


#create function for drawing background
def draw_bg():
    screen.fill(GREEN)
    width = sky_img.get_width()
    for x in range(4):
        screen.blit(sky_img, ((x * width) - scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x * width) - scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * width) - scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))

#draw grid
def draw_grid():
    #vertical lines
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
    #horizontal lines
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))


#function for drawing the world tiles
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))

"""def draw_tile_panel():
    global current_tile
    # Dessiner le fond du panneau de tuiles
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

    # Dessiner les tuiles pour la page actuelle
    start_index = current_page * tiles_per_page
    end_index = min(start_index + tiles_per_page, len(img_list))
    button_col = 0
    button_row = 0

    for i in range(start_index, end_index):
        tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
        if tile_button.draw(screen):
            current_tile = i
        button_col += 1
        if button_col == 3:
            button_row += 1
            button_col = 0

    # Mettre en surbrillance la tuile sélectionnée
    if current_tile >= start_index and current_tile < end_index:
        tile_index = current_tile - start_index
        selected_button = button.Button(SCREEN_WIDTH + (75 * (tile_index % 3)) + 50, 75 * (tile_index // 3) + 50, img_list[current_tile], 1)
        pygame.draw.rect(screen, RED, selected_button.rect, 3)"""




def draw_tiles_for_current_page():
    global current_tile_buttons
    # Effacer les boutons de tuiles actuels pour les remplacer par de nouveaux.
    current_tile_buttons = []
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

    # Calculer les indices de début et de fin pour les tuiles à dessiner
    start_index = current_page * tiles_per_page
    end_index = min(start_index + tiles_per_page, TILE_TYPES)
    button_col = 0
    button_row = 0

    for i in range(start_index, end_index):
        tile_x = (button_col * (TILE_SIZE + 10)) + SCREEN_WIDTH + 80  # Ajoutez une marge si nécessaire
        tile_y = (button_row * (TILE_SIZE + 10)) + 80  # Ajoutez une marge si nécessaire
        tile_image = img_list[i]
        tile_button = button.Button(tile_x, tile_y, tile_image, 1, start_index + (i - start_index) )
        current_tile_buttons.append(tile_button)  # Ajouter le bouton de tuile à la liste
        tile_button.draw(screen)
        button_col += 1
        if button_col == 3:
            button_col = 0
            button_row += 1

# Mettre en surbrillance la tuile sélectionnée
def highlight_selected_tile():
    if current_tile_buttons:
        for button in current_tile_buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, RED, button.rect, 3)
                return button
    
    return None


#create buttons
save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)
#make a button list
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0


run = True

while run:

    clock.tick(FPS)

    draw_bg()
    draw_grid()
    draw_world()

    draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text('Press UP or DOWN to change level', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

    # save and load data
    if save_button.draw(screen):
        with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in world_data:
                writer.writerow(row)

    if load_button.draw(screen):
        scroll = 0
        with open(f'level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)




    # draw tile panel and tiles
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

    '''
    # choose a tile
    start_index = current_page * tiles_per_page
    end_index = min(start_index + tiles_per_page, len(button_list))

    for button_count, i in enumerate(button_list[start_index:end_index]):
        button_col = button_count % 3
        button_row = button_count // 3
        if i.draw(screen):
            current_tile = start_index + button_count

    # highlight the selected tile
    if start_index <= current_tile < end_index:
        pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)
    '''


    # scroll the map
    if scroll_left and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
        scroll += 5 * scroll_speed

    # add new tiles to the screen
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE

    if pygame.mouse.get_pressed()[0] == 1:
        if highlighted_button != None:
            current_tile = highlighted_button.tile_index


    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1
            if event.key == pygame.K_1:
                current_page = (current_page - 1) % total_pages
            if event.key == pygame.K_2:
                current_page = (current_page + 1) % total_pages
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 5
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False



    draw_tiles_for_current_page()
    highlighted_button = highlight_selected_tile()
    pygame.display.update()


pygame.quit()
