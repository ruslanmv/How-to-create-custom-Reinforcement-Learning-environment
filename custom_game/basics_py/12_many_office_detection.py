import pygame, random

#Initialize Pygame
pygame.init()



#Create a display surface
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300


display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

WHITE = (255, 255, 255)


pygame.display.set_caption("Office Detection!")


#Set FPS amnd clock
FPS = 60
clock = pygame.time.Clock()

#Set game values
VELOCITY = 5

#Load images
man_image = pygame.image.load("man_right.png")
man_rect = man_image.get_rect()
man_rect.topleft = (25, 25)

desktop_image = pygame.image.load("desktop.png")
desktop_rect = desktop_image.get_rect()
desktop_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

#The main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Get a list of all keys currently being pressed down
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and man_rect.left > 0:
        man_rect.x -= VELOCITY
    if keys[pygame.K_RIGHT] and man_rect.right < WINDOW_WIDTH:
        man_rect.x += VELOCITY
    if keys[pygame.K_UP] and man_rect.top > 0:
        man_rect.y -= VELOCITY
    if keys[pygame.K_DOWN] and man_rect.bottom < WINDOW_HEIGHT:
        man_rect.y += VELOCITY

    #Check for collision between two rects
    if man_rect.colliderect(desktop_rect):
        print("HIT")
        desktop_rect.x = random.randint(0, WINDOW_WIDTH - 32)
        desktop_rect.y = random.randint(0, WINDOW_HEIGHT - 32)

    #Fill display surface
    #display_surface.fill((0, 0, 0))
    #Give a background color to the display
    display_surface.fill(WHITE)

    #Draw rectangles to represent the rect's of each object
    pygame.draw.rect(display_surface, (0, 255, 0), man_rect, 1)
    pygame.draw.rect(display_surface, (255, 255, 0), desktop_rect, 1)

    #Blit assets
    display_surface.blit(man_image, man_rect)
    display_surface.blit(desktop_image, desktop_rect)

    #Update dispaly
    pygame.display.update()

    #Tick the clock
    clock.tick(FPS)

#End the game
pygame.quit()