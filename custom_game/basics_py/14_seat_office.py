import pygame, random

#Initialize Pygame
pygame.init()



#Create a display surface
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768


display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
WHITE = (255, 255, 255)




import random
import pickle
with open('seats.pkl', 'rb') as f:
    seats_coordinates = pickle.load(f)


pygame.display.set_caption("Office Detection!")


#Set FPS amnd clock
FPS = 60
clock = pygame.time.Clock()

#Set game values
VELOCITY = 5

#Load images
man_image = pygame.image.load("point_yellow.png")
man_rect = man_image.get_rect()
man_rect.topleft = (25, 25)

desktop_image = pygame.image.load("point_blue.png")
desktop_rect = desktop_image.get_rect()

desktop_pos_1=random.choice(seats_coordinates)
desktop_rect.center = (desktop_pos_1[0], desktop_pos_1[1])



desktop_image2 = pygame.image.load("point_red.png")
desktop_rect2 = desktop_image2.get_rect()
desktop_pos_2=random.choice(seats_coordinates)
desktop_rect2.center = (desktop_pos_2[0], desktop_pos_2[1])



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
        print("HIT NOT DESIRED")
        #Respawn in a new position
        desktop_pos_new_1=random.choice(seats_coordinates)
        
        desktop_rect.x = desktop_pos_new_1[0]
        desktop_rect.y = desktop_pos_new_1[1]

    #Check for collision between two rects
    if man_rect.colliderect(desktop_rect2):
        print("HIT DESIRED")
        #Respawn in a new position
        desktop_pos_new_2=random.choice(seats_coordinates)
        desktop_rect2.x = desktop_pos_new_2[0]
        desktop_rect2.y = desktop_pos_new_2[1]

  
  
  
    #Fill display surface
    #display_surface.fill((0, 0, 0))

    bg = pygame.image.load("background.png")

   

    #Give a background color to the display
    #display_surface.fill(WHITE)
    #INSIDE OF THE GAME LOOP
    display_surface.blit(bg, (0, 0))

    #Draw rectangles to represent the rect's of each object
    pygame.draw.rect(display_surface, (0, 255, 0), man_rect, 1)
    pygame.draw.rect(display_surface, (255, 255, 0), desktop_rect, 1)
    pygame.draw.rect(display_surface, (255, 255, 0), desktop_rect2, 1)


    #Blit assets
    display_surface.blit(man_image, man_rect)
    display_surface.blit(desktop_image, desktop_rect)
    display_surface.blit(desktop_image2, desktop_rect2)



    #Update dispaly
    pygame.display.update()

    #Tick the clock
    clock.tick(FPS)

#End the game
pygame.quit()