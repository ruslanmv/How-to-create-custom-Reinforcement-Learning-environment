from src.libs import *
from src.configs import *

class WorkerEnvGym(gym.Env):
    metadata = {'render_modes': ["human"]}

    def __init__(self, frame_size_x=200, frame_size_y=200):
        #  super(WorkerEnvGym, self).__init__()
        self.action_space = spaces.Discrete(4)
        self.frame_size_x = frame_size_x
        self.frame_size_y = frame_size_y
        self.game_window = pygame.display.set_mode((self.frame_size_x, self.frame_size_y))
        self.reset()
        self.STEP_LIMIT = 1000
        self.sleep = 0
        pass

    def step(self, action):
        scoreholder = self.score
        reward = 0
        self.direction = WorkerEnvGym.change_direction(action, self.direction)
        self.agent_pos, changed_pos = WorkerEnvGym.move(self.direction, self.agent_pos)
        if changed_pos:
            self.agent_pos.insert(0, list(self.agent_pos))
            self.agent_pos.pop()

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
    def move(direction, agent_pos):
        changed_pos = False
            
        if direction == 'UP' and worker_pos[1] - 10 >= 0:
            agent_pos[1] -= 10
            changed_pos = True
        if direction == 'DOWN' and agent_pos[1] + 10 < self.frame_size_y:
            agent_pos[1] += 10
            changed_pos = True
        if direction == 'LEFT' and agent_pos[0] - 10 >= 0:
            agent_pos[0] -= 10
            changed_pos = True
        if direction == 'RIGHT' and agent_pos[0] + 10 < self.frame_size_x:
            agent_pos[0] += 10
            changed_pos = True
            
        return agent_pos, changed_pos
    
    def update_game_state(self):
        self.game_window.fill(BLACK)
        for pos in self.agebt_body:
            pygame.draw.rect(self.game_window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))
    
    def get_image_array_from_game(self):
        img = array3d(display.get_surface())
        img = np.swapaxes(img, 0, 1)
        return img

    def game_over(self, reward):
        if self.steps >= 1000:
            return 0, True
        
        return reward, False

    def reset(self):
        self.game_window.fill(BLACK)
        self.agent_pos = [100, 50]
        self.agent_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

        self.direction = "RIGHT"
        self.change_to = self.direction
        self.score = 0
        self.steps = 0
        img = array3d(display.get_surface())
        img = np.swapaxes(img, 0, 1)
        return img

    def render(self, mode=f'{RENDER_MODE}'):
        if mode == f"{RENDER_MODE}":
            display.update()
            
    def close(self):
        pass
