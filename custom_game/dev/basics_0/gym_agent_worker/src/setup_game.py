from src.libs import *
from src.worker_env import WorkerEnv
from src.configs import *

# =============================================================================================== #
# Setup Game
# =============================================================================================== #

def setup_game() -> dict:
    """Setup the game.
    Return:
    ---
    `game_config`: dict.\n
    """
    # Create an instance of our game environment
    worker_env = WorkerEnv(WIDTH, HEIGHT)   

    # FPS (frames per second) controller
    fps_controller = pygame.time.Clock()

    # Checks for errors encountered
    check_errors = pygame.init()

    # Initialise game window
    pygame.display.set_caption('Worker Booker')
    return {
        'game_env': worker_env,
        'fps_controller': fps_controller,
        'difficulty': DIFFICULTY,
        'check_errors': check_errors
    }
