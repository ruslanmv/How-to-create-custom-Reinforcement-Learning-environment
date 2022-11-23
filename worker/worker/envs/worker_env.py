import time
import numpy as np
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import pygame, sys, time, random
from pygame.surfarray import array3d
from pygame import display
## Sets up colors for the game using RGB Codes
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)

class WorkerEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.action_space = spaces.Discrete(4)
        self.frame_size_x = 200
        self.frame_size_y = 200
        self.game_window = pygame.display.set_mode((self.frame_size_x, self.frame_size_y))
        self.reset()
        self.STEP_LIMIT = 1000
        self.sleep = 0

    def step(self, action):
        scoreholder = self.score
        reward = 0
        self.direction = WorkerEnv.change_direction(action, self.direction)
        self.Worker_pos = WorkerEnv.move(self.direction, self.Worker_pos)
        self.Worker_body.insert(0, list(self.Worker_pos))

        reward = self.seat_handler()

        self.update_game_state()

        reward, done = self.game_over(reward)

        img = self.get_image_array_from_game()
        info = {"score": self.score}
        self.steps += 1
        time.sleep(self.sleep)
        return img, reward, done, info

    @staticmethod
    def change_direction(action, direction):
        if action == 0 and direction != "DOWN":
            direction = 'UP'
        if action==1 and direction != "UP":
            direction = 'DOWN'
        if action==2 and direction != "RIGHT":
            direction = 'LEFT'
        if action==3 and direction != "LEFT":
            direction = 'RIGHT'
        return direction

    @staticmethod
    def move(direction, Worker_pos):
        if direction == 'UP':
            Worker_pos[1] -= 10
        if direction == 'DOWN':
            Worker_pos[1] += 10
        if direction == 'LEFT':
            Worker_pos[0] -= 10
        if direction == 'RIGHT':
            Worker_pos[0] += 10
        return Worker_pos


    def eat(self):
        return self.Worker_pos[0] == self.seat_pos[0] and self.Worker_pos[1] == self.seat_pos[1]
    
    def spawn_seat(self):
        return [random.randrange(1, (self.frame_size_x//10)) * 10, random.randrange(1, (self.frame_size_y//10)) * 10]

    def seat_handler(self):
        if self.eat():
            self.score += 1
            reward = 1
            self.seat_spawn = False
        else:
            self.Worker_body.pop()
            reward = 0

        if not self.seat_spawn:
            self.seat_pos = self.spawn_seat()
        self.seat_spawn = True

        return reward

    def update_game_state(self):
        self.game_window.fill(BLACK)
        for pos in self.Worker_body:
            pygame.draw.rect(self.game_window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.draw.rect(self.game_window, WHITE, pygame.Rect(self.seat_pos[0], self.seat_pos[1], 10, 10))

    def get_image_array_from_game(self):
        img = array3d(display.get_surface())
        img = np.swapaxes(img, 0, 1)
        return img

    def game_over(self, reward):
        if self.Worker_pos[0] < 0 or self.Worker_pos[0] > self.frame_size_x-10:
            return -1, True
        if self.Worker_pos[1] < 0 or self.Worker_pos[1] > self.frame_size_y-10:
            return -1, True

        for block in self.Worker_body[1:]:
            if self.Worker_pos[0] == block[0] and self.Worker_pos[1] == block[1]:
                return -1, True
        if self.steps >= 1000:
            return 0, True
        
        return reward, False



    def reset(self):
        self.game_window.fill(BLACK)
        self.Worker_pos = [100, 50]
        self.Worker_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
        self.seat_pos = self.spawn_seat()
        self.seat_spawn = True

        self.direction = "RIGHT"
        self.change_to = self.direction
        self.score = 0
        self.steps = 0
        img = array3d(display.get_surface())
        img = np.swapaxes(img, 0, 1)
        return img


    def render(self, mode='human'):
        if mode == "human":
            display.update()
            
    def close(self):
        pass

