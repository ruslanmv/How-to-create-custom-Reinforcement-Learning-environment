from src.libs import *
from src.worker_env import WorkerEnv
from src.configs import *

# =============================================================================================== #
# Setup Game
# =============================================================================================== #

def setup_game():
    worker_env = WorkerEnv(1024, 768)

    # This is technically a FPS Refresh rate
    # Higher number means faster refresh, thus faster Worker movement, meaning harder game play
    difficulty = 10

    # FPS (frames per second) controller
    fps_controller = pygame.time.Clock()

    # Checks for errors encountered
    check_errors = pygame.init()

    # Initialise game window
    pygame.display.set_caption('Worker Booker')
    return {
        'game_env': worker_env,
        'fps_controller': fps_controller,
        'difficulty': difficulty,
        'check_errors': check_errors
    }
