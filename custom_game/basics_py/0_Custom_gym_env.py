import pygame, sys, time, random
from pygame.surfarray import array3d
import random
import pickle
## Sets up colors for the game using RGB Codes
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0) 
with open('seats.pkl', 'rb') as f:
    seats_coordinates = pickle.load(f)

class PersonEnv():
    
    def __init__(self,frame_size_x,frame_size_y):
        '''
        Defines the initial game window size
        '''
        self.frame_size_x = frame_size_x
        self.frame_size_y = frame_size_y
        self.game_window = pygame.display.set_mode((self.frame_size_x, self.frame_size_y))        
        self.reset()
    
    def reset(self):
        '''
        Resets the game, along with the default Person size and spawning seat.
        '''
        #self.game_window.fill(BLACK)


        self.Person_pos = [100, 50]
        self.Person_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
        self.seat_pos = self.spawn_seat()
        
        self.seat_spawn = True

        self.direction = "RIGHT"
        self.action = self.direction
        self.score = 0
        self.steps = 0
        print("Game Reset.")
    
    def change_direction(self,action,direction):
        '''
        Changes direction based on action input. 
        Checkes to make sure Person can't go back on itself.
        '''
        
        if action == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if action == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if action == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if action == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'
            
        return direction
    
    def move(self,direction,Person_pos):
        '''
        Updates Person_pos list to reflect direction change.
        '''
            
        if direction == 'UP':
            Person_pos[1] -= 10
        if direction == 'DOWN':
            Person_pos[1] += 10
        if direction == 'LEFT':
            Person_pos[0] -= 10
        if direction == 'RIGHT':
            Person_pos[0] += 10
            
        return Person_pos
    
    def eat(self):
        '''
        Returns Boolean indicating if Person has "taken" the red seat square
        '''
        return self.Person_pos[0] == self.seat_pos[0] and self.Person_pos[1] == self.seat_pos[1]
    
   
    def spawn_seat(self):
        '''
        Spawns seat in a random location on window size
        '''

        
        #seat_pos_1=random.choice(seats_coordinates)
        #return[seat_pos_1[0], seat_pos_1[1]]
        return [random.randrange(1, (self.frame_size_x//10)) * 10, random.randrange(1, (self.frame_size_y//10)) * 10]
    
    def human_step(self,event):   
        '''
        Takes human keyboard event and then returns it as an action string
        '''
        
        action = None
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        ################################################ 
        ########## CONVERT KEYPRESS TO DIRECTION ###### 
        ############################################## 
        elif event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_UP:
                action = 'UP'
            if event.key == pygame.K_DOWN:
                action = 'DOWN'
            if event.key == pygame.K_LEFT:
                action = 'LEFT'
            if event.key == pygame.K_RIGHT:
                action = 'RIGHT'
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                
        return action
    
    
    
    def display_score(self,color, font, size):
        '''
        Updates the score in top left
        '''
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (self.frame_size_x/10, 15)
        self.game_window.blit(score_surface, score_rect)
        
    def game_over(self):
        '''
        Checks if the Person has touched the bounding box or itself
        '''
        
        # TOUCH BOX
        #if self.Person_pos[0] < 0 or self.Person_pos[0] > self.frame_size_x-10:
        #    self.end_game()
        #if self.Person_pos[1] < 0 or self.Person_pos[1] > self.frame_size_y-10:
        #    self.end_game()

        # TOUCH OWN BODY
        #for block in self.Person_body[1:]:
        #    if self.Person_pos[0] == block[0] and self.Person_pos[1] == block[1]:
        #        self.end_game()
 


    def end_game(self):
        '''
        
        '''
        message = pygame.font.SysFont('arial', 45)
        message_surface = message.render('Game has Ended.', True, RED)
        message_rect = message_surface.get_rect()
        message_rect.midtop = (self.frame_size_x/2, self.frame_size_y/4)
        self.game_window.fill(BLACK)
        self.game_window.blit(message_surface, message_rect)
        self.display_score(RED, 'times', 20)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()


Person_env = PersonEnv(1024,768)

# This is technically a FPS Refresh rate
# Higher number means faster refresh, thus faster Person movement, meaning harder game play
difficulty = 10


# FPS (frames per second) controller
fps_controller = pygame.time.Clock()

# Checks for errors encountered
check_errors = pygame.init()


# Initialise game window
pygame.display.set_caption('Person Booker') 

############## Custom additons ################
import random
import pickle
with open('seats.pkl', 'rb') as f:
    seats_coordinates = pickle.load(f)

#Create a display surface
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

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

###################################
#The main game loop
running = True
while running:
    
    # Check Input from Human Step 
    for event in pygame.event.get():
        
        Person_env.action = Person_env.human_step(event)
    
        #if event.type == pygame.QUIT:
        #    running = False


    # Check for Direction change based on action
    Person_env.direction = Person_env.change_direction(Person_env.action,Person_env.direction)
    print(Person_env.Person_pos)

####################à
    
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




######################

    #Update Person Position
    Person_env.Person_pos = Person_env.move(Person_env.direction,Person_env.Person_pos)


    # Check to see if we ate some seat
    Person_env.Person_body.insert(0, list(Person_env.Person_pos))
    if Person_env.eat():
        Person_env.score += 1
        Person_env.seat_spawn = False
    else:
        Person_env.Person_body.pop()

    # Check to see if we need to spawn new seat 
    if not Person_env.seat_spawn:
        Person_env.seat_pos = Person_env.spawn_seat()
    Person_env.seat_spawn = True

    
   # Person_env.game_window.fill(BLACK)

    bg = pygame.image.load("background.png")
    #INSIDE OF THE GAME LOOP
    Person_env.game_window.blit(bg, (0, 0))

    ################
    #Draw rectangles to represent the rect's of each object
    pygame.draw.rect(Person_env.game_window, (0, 255, 0), man_rect, 1)
    pygame.draw.rect(Person_env.game_window, (255, 255, 0), desktop_rect, 1)
    pygame.draw.rect(Person_env.game_window, (255, 255, 0), desktop_rect2, 1)


    #Blit assets
    Person_env.game_window.blit(man_image, man_rect)
    Person_env.game_window.blit(desktop_image, desktop_rect)
    Person_env.game_window.blit(desktop_image2, desktop_rect2)

    #####    
    # Draw the Person
    
    for pos in Person_env.Person_body:
        pygame.draw.rect(Person_env.game_window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))
        
    # Draw seat
    pygame.draw.rect(
        
                     Person_env.game_window, RED, 
                     pygame.Rect(Person_env.seat_pos[0], 
                     Person_env.seat_pos[1], 10, 10)
        
                     )

    # Check if we lost
    Person_env.game_over()
    
    

    Person_env.display_score(BLACK, 'consolas', 20)
    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(difficulty)
    img = array3d(Person_env.game_window)       