import gym
from gym import spaces
import numpy as np
import matplotlib.pyplot as plt
import pygame
from pygame import display
from pygame.surfarray import array3d
import random
import pandas as pd
from PIL import Image
import time
training=False

df= pd.read_csv("test.csv")
feature1=df['island'].max()
feature2=df['project'].max()
feature3=df['energy_consumption'].max()
feature4=df['emp_project'].max()
feature5=df['emp_energy_consumption'].max()
feature6=df['occupied'].max()

max_colors=df['island'].nunique()
low_x=int(df['x_coord'].min())
high_x=int(df['x_coord'].max())
low_y=int(df['y_coord'].min())
high_y=int(df['y_coord'].max())
possible_clicks=df.shape[0]
pos_x=possible_clicks
pos_y=possible_clicks
max_sit=possible_clicks

# get image
filepath = "bg.jpg"
img_bg = Image.open(filepath)
# get width and height
width = img_bg.width
height = img_bg.height
  
font_color=(0,50,250)
WHITE = pygame.Color(255, 255, 255)
RED = (200,0,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

#Load images
#To the image we assing a kind of gym object
worker_pos=[25,25]
#Target image and position
position_coordinates=[(50,50),
                      (100,50),
                      (150,50)]

target_rects={}
target_images={}
counts = df.groupby(['island'])['island'].count()
reward_dict=counts.to_dict()

def convert_colormap_to_hex(cmap, x, vmin=0, vmax=1):
    """
    Example::
        >>> seaborn.palplot(seaborn.color_palette("RdBu_r", 7))
        >>> colorMapRGB = seaborn.color_palette("RdBu_r", 61)
        >>> colormap = seaborn.blend_palette(colorMapRGB, as_cmap=True, input='rgb')
        >>> [convert_colormap_to_hex(colormap, x, vmin=-2, vmax=2) for x in range(-2, 3)]
        ['#09386d', '#72b1d3', '#f7f6f5', '#e7866a', '#730421']
    """
    norm = colors.Normalize(vmin, vmax)
    color_rgb = plt.cm.get_cmap(cmap)(norm(x))
    color_hex = colors.rgb2hex(color_rgb)
    return color_hex

import  seaborn
from matplotlib import colors
from PIL import ImageColor
colorMapRGB = seaborn.color_palette("RdBu_r", max_colors)
colormap = seaborn.blend_palette(colorMapRGB, as_cmap=True, input='rgb')
cmap_list=[convert_colormap_to_hex(colormap, x, vmin=-int(max_colors/2)-1, vmax=int(max_colors/2)+1) for x in range(-int(max_colors/2)-1, int(max_colors/2)+1)]


class MyEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    def __init__(self):
        # There are two actions, first will get reward of 1, second reward of -1. 
        self.action_space = spaces.Discrete(possible_clicks)
        self.observation_space = gym.spaces.Dict(
     {"feature1": gym.spaces.Box(low=0, high=feature1, shape=(1,), dtype=np.uint8),
     "y_position": gym.spaces.Box(low=low_y, high=high_y, shape=(1,), dtype=np.uint8),
     "x_position": gym.spaces.Box(low=low_x, high=high_x, shape=(1,), dtype=np.uint8)
     }
        )
        # We inizialize the display
        self.frame_size_x = width # high_x
        self.frame_size_y = height# high_y
        self.game_window = pygame.display.set_mode((self.frame_size_x, self.frame_size_y))  
        self.reset()
  
    def reset(self):
        self.game_window.fill(WHITE)
        self.state = None
        self.steps = 0
        self.worker_pos=[25,25] 
        self.score = 0
        self.steps = 0
        action=(0,0)
        img = array3d(display.get_surface())
        img = np.swapaxes(img, 0, 1)
        self.STEP_LIMIT = 1000
        #To the image we assing a kind of gym object
        self.worker_rect=pygame.draw.circle(self.game_window,BLUE,(self.worker_pos[0], self.worker_pos[1]),6) # DRAW CIRCLE
        # Moreover we add a position in the screen display
        self.target_rects={} 
        n_space=df.shape[0]
        for num in range(n_space):
            targets=int(df['x_coord'][num]), int(df['y_coord'][num])
            numero_cluster=df['island'][num]
            cmap_color=cmap_list[numero_cluster-1]
            target_images[num] = pygame.draw.circle(self.game_window,cmap_color,(targets[0], targets[1]),6) # DRAW CIRCLE
            self.target_rects[num] = target_images[num]
            #print('Initial positions',targets)
            self.target_rects[num].center = targets
        # Adding text
        pygame.init()
        self.font_color=(0,50,250)                                       # Step 1  Color RGB code
        self.font_obj=pygame.font.Font("C:\Windows\Fonts\Arial.ttf",20)  # Step 2  Select the font type
        # Render the objects
        self.text_obj=self.font_obj.render("Reward:",True,self.font_color) # Step 3  Creation of object text        
        #state, reward, done, info = self.step(action) 
        return img        
        #return state, reward, done, info
        
    def reward_value(self,worker,target,num):
        
        #print(Reward check: )
        #Check for collision between two rects            
        if worker.colliderect(target):
            '''
            Reward 1 - The more dense is the cluster more reward  
            Gives the value of the island   number of seats
                0    2
                1    4
                2    4
                3    4
                4    1
            '''
            number_island=df['island'].iloc[num]
            reward1=reward_dict[number_island]

            '''
            Reward 2 - Check if is occupied
                0 - occupied
                1 - free
            '''
            is_occupied=df['occupied'].iloc[num]
           
            '''
            Reward 3 - More neighbors more reward
            '''
            reward3=len(df[(df['island']==number_island) & (df['occupied']==0 )])
            reward=(reward1+reward3)*is_occupied
            
            if is_occupied == 0:
                if training:  print('is_occupied',is_occupied)
            else:
                if training:  print('reward',reward)
            
            return reward
        
        else:
            
            reward = 0
            return reward
            
    def step(self, action):
        reward = 0
        total_reward=0
        # Check if variable is  tuple
        # using type()
        #res = type(action) is tuple       
        # Inside gym the test need tuples and not int
        
        if (type(action) == int) or (isinstance(action, np.int64)) :
            action_n=int(action)
            if training: print('action_n',action_n)
            action=int(df['x_coord'][action_n]), int(df['y_coord'][action_n])
        
        self.worker_pos = action
        if training: print('The action is inside step:', action, type(action))
        rewards=[]
        # We update the state of worker_rect and image
        self.update_game_state() 
        
        
        # regardless of the action, game is done after a single step
        if action != None:
            if training:  print("The action is :", action)  
            n_space=df.shape[0]
            for num in range(n_space):
                reward = self.reward_value(self.worker_rect,self.target_rects[num],num)
                #print('num',num)

                if reward !=0:
        
                    #print("The worker rect is :",self.worker_rect)
                    #print("The target rect is :",self.target_rects[num] ) 
                    rewards.append(reward)
                    #print("rewards",rewards)
                    
        if len(rewards) < 1:
            reward=0
        else:
            reward=rewards[0]

        if training == False:
            # Render the objects
            self.text_obj=self.font_obj.render("Reward :" + str(reward),True,self.font_color) # Step 3  Creation of object text
            #Display text
            self.game_window.blit(self.text_obj,(300,0))         
                          
        img = self.get_image_array_from_game()
        
        info = {}
        reward_tmp, done = self.game_over(reward)
        #done = True ### Testing without Accumulative
        total_reward=total_reward+reward_tmp ### Accumulative
        
        if training:  print('reward: {}, done: {}, info: {}, step: {}'.format(reward, done, info,self.steps))
        self.steps += 1
        return img, total_reward, done, info

    
    def worker_step(self,event):   
        '''
        Takes human keyboard event and then returns it as an action string
        '''
        action = None
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        #Move based on mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            #print(event)
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]

            #'CLICK'
            action = mouse_x, mouse_y
        
        #Drag the object when the mouse button is clicked
        if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
            #print(event)
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]
    
            #'CLICK'
            action = mouse_x, mouse_y
        
        elif event.type == pygame.KEYDOWN:
        
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))                       
        return action    
    
    def update_game_state(self):
        #We fill the screen to white
        if training != True:
            self.game_window.fill(WHITE)
        else:    
            bg = pygame.image.load("bg.jpg")
            #Give a background color to the display
            self.game_window.blit(bg, (0, 0))
        # -------------WORKER--------------
        
        #if type(self.worker_pos) == int:
        #    action_n=self.worker_pos
        #    print('action_n in update is:',action_n)
        #    action=int(df['x_coord'][action_n]), int(df['y_coord'][action_n])
        #    self.worker_pos=action    
        
        if training: 
            print('self.worker_pos:',self.worker_pos)
            print('worker_pos',self.worker_pos[0],self.worker_pos[1])
        
        self.worker_rect.x=self.worker_pos[0]
        self.worker_rect.y=self.worker_pos[1]
        #Draw rectangles to represent the rect's of each object
        self.worker_rect=pygame.draw.circle(self.game_window,BLUE,(self.worker_rect.x,self.worker_rect.y),6) # DRAW CIRCLE
        
        #-------------- Multiple points TARGETS------------------
        n_space=df.shape[0]
        for num in range(n_space):
            numero_cluster=df['island'][num]
            cmap_color=cmap_list[numero_cluster-1]
            occupied=df['occupied'][num]
            if occupied == 0:
                color=RED
            else:
                color=GREEN
            pygame.draw.circle(self.game_window,color,(self.target_rects[num].x,self.target_rects[num].y),6) # DRAW CIRCLE
            
    def get_image_array_from_game(self):
        img = array3d(display.get_surface())
        #Preprocessing of channels ( needed for tensorflow)
        img = np.swapaxes(img, 0, 1)
        return img    
   
    def render(self, mode='human'):
        if mode == "human":
            display.update()        
    def close(self):
        pass
    
    def game_over(self, reward):
        if (reward == 0) or ( self.steps >= 20): 
            
            #self.end_game()
            
            return -1, True

        return reward, False
    
    
    def end_game(self):

        message = pygame.font.SysFont('arial', 20)
        message_surface = message.render('Ciao! Perché non ti siedi qua?' +' '+str("s"), True, RED)
        message_rect = message_surface.get_rect()
        message_rect.midtop = (self.frame_size_x / 2, self.frame_size_y / 4)
        self.game_window.fill(BLACK)
        self.game_window.blit(message_surface, message_rect)
        pygame.display.flip()
        #time.sleep(20)
        pygame.quit()
        sys.exit()    