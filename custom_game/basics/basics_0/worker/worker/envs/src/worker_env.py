from src.libs import *
from src.configs import *

class WorkerEnv():
    
    def __init__(self,frame_size_x, frame_size_y):
        '''
        Defines the initial game window size
        '''
        self.frame_size_x = frame_size_x
        self.frame_size_y = frame_size_y
        self.game_window = pygame.display.set_mode((self.frame_size_x, self.frame_size_y))        
        self.reset()
    
    def reset(self):
        '''
        Resets the game, along with the default Worker size and spawning seat.
        '''
        self.game_window.fill(BLACK)
        self.worker_pos = [100, 50]
        self.worker_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

        self.direction = "RIGHT"
        self.action = self.direction
        self.score = 0
        self.steps = 0
        print("Game Reset.")
    
    def change_direction(self,action,direction):
        '''
        Changes direction based on action input. 
        Checkes to make sure Worker can't go back on itself.
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
    
    def move(self,direction, worker_pos):
        '''
        Updates Worker_pos list to reflect direction change.
        '''
        changed_pos = False
            
        if direction == 'UP' and worker_pos[1] - 10 >= 0:
            worker_pos[1] -= 10
            changed_pos = True
        if direction == 'DOWN' and worker_pos[1] + 10 < self.frame_size_y:
            worker_pos[1] += 10
            changed_pos = True
        if direction == 'LEFT' and worker_pos[0] - 10 >= 0:
            worker_pos[0] -= 10
            changed_pos = True
        if direction == 'RIGHT' and worker_pos[0] + 10 < self.frame_size_x:
            worker_pos[0] += 10
            changed_pos = True
            
        return worker_pos, changed_pos
    
    def worker_step(self, event):   
        '''
        Takes human keyboard event and then returns it as an action string
        '''
        
        action = None
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
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
        
    def win(self, target):
        # if self.worker_pos[0] == target[1] and self.worker_pos[1] == target[0]:
        head_pos = self.worker_body[0]
        head = pygame.Rect(head_pos[0], head_pos[1], 10, 10)
        if head.colliderect(target):
            self.end_game()

    def game_over(self,):
        '''
        Checks if the Worker has touched the bounding box or itself
        '''
        
        # TOUCH BOX
        #if self.Worker_pos[0] < 0 or self.Worker_pos[0] > self.frame_size_x-10:
        #    self.end_game()
        #if self.Worker_pos[1] < 0 or self.Worker_pos[1] > self.frame_size_y-10:
        #    self.end_game()

        # TOUCH OWN BODY
        #for block in self.Worker_body[1:]:
        #    if self.Worker_pos[0] == block[0] and self.Worker_pos[1] == block[1]:
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
