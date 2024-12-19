import pygame

pygame.init()

screen = pygame.display.set_mode((1792, 1024))

# Chargement et mise à l'échelle des images
image = pygame.image.load("tile_0000.png").convert_alpha()
background = pygame.image.load("fond.webp").convert()
image = pygame.transform.scale(image, (96, 96))

# Initialisation du rectangle de l'image
rect = image.get_rect()
rect.x = 400
rect.y = 920

clock = pygame.time.Clock()
continuer = True
moveSpeed = 6
JumpForce = 15
Jumping = False
doubleJump = False  
Y_Velocity = 0
Y_Gravity = 1
Ground_Y = rect.y


while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not Jumping:  
                    Jumping = True
                    doubleJump = True 
                    Y_Velocity = JumpForce
                elif doubleJump:  
                    Y_Velocity = JumpForce  
                    doubleJump = False  

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT] and rect.left > 0:
        rect.x -= moveSpeed
    if pressed[pygame.K_RIGHT] and rect.right < 1792:
        rect.x += moveSpeed

    if Jumping:
        rect.y -= Y_Velocity
        Y_Velocity -= Y_Gravity
        if rect.y >= Ground_Y:  
            rect.y = Ground_Y
            Jumping = False
            doubleJump = False 
            Y_Velocity = 0

    screen.blit(background, (0, 0))
    screen.blit(image, rect)
    pygame.draw.rect(screen, (255, 255, 255), rect, 2)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
