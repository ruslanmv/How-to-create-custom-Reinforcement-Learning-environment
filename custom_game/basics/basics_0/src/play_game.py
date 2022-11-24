from src.libs import *
from src.worker_env import WorkerEnv
from src.configs import *

# =============================================================================================== #
# Play Game Utils
# =============================================================================================== #

def _check_if_win(game_env: WorkerEnv) -> None:
    if TARGET_COORDS:
        game_env.win(target=TARGET_RECT)
        game_env.display_score(BLACK, 'consolas', 20)


def _check_if_lost(game_env: WorkerEnv) -> None:
    game_env.game_over()
    game_env.display_score(BLACK, 'consolas', 20)


def _refresh_game(game_env: WorkerEnv, fps_controller, difficulty) -> np.ndarray:
    # Refresh game screen
    
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(difficulty)
    img = array3d(game_env.game_window)     
    return img


def _update_and_draw_worker_pos(game_env: WorkerEnv) -> None:

    # Check for Direction change based on action
    game_env.direction = game_env.change_direction(game_env.action, game_env.direction)
    if SHOW_WORKER_POS:
        print(game_env.worker_pos)
    
    #Get a list of all keys currently being pressed down
    keys = pygame.key.get_pressed()

    # Update Worker Position
    game_env.worker_pos, changed_pos = game_env.move(game_env.direction, game_env.worker_pos)
    if changed_pos:
        game_env.worker_body.insert(0, list(game_env.worker_pos))
        game_env.worker_body.pop()

    
    for pos in game_env.worker_body:
        pygame.draw.rect(game_env.game_window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))


def _check_inputs_from_game_step(game_env: WorkerEnv) -> bool:
    # Check Input from Game Step 
    for event in pygame.event.get():        
        game_env.action = game_env.worker_step(event)
        if event.type == pygame.QUIT:
            return False
    return True


def _clear_screen(game_env: WorkerEnv) -> None:
    if FLAG_BLACK_BG and NO_SEATS_FLAG:
        game_env.game_window.fill(BLACK)
    elif SEATS_FLAG:
        bg = pygame.image.load(BACKGROUND_IMAGE)
        game_env.game_window.blit(bg, (0, 0))
        for ii, pos in enumerate(SEATS_COORDS):
            if ii == TARGET_SEAT:
                pygame.draw.rect(game_env.game_window, TAREGT_COLOR, pygame.Rect(pos[0], pos[1], 10, 10))
            else:
                pygame.draw.rect(game_env.game_window, RED, pygame.Rect(pos[0], pos[1], 10, 10))
    else:
        game_env.game_window.fill(BLACK)
        pos = TARGET_COORDS
        pygame.draw.rect(game_env.game_window, TAREGT_COLOR, pygame.Rect(pos[0], pos[1], 10, 10))


# =============================================================================================== #
# Play Game
# =============================================================================================== #

def play_game(game_config: dict) -> None:
    """Play the game.
    Args:
    ---
    `game_config`: input dict.\n
    """

    # Unbox inpuit config
    game_env = game_config["game_env"]
    fps_controller = game_config["fps_controller"]
    difficulty = game_config["difficulty"]

    # Run main loop
    running = True
    while running:
        # Clear screen
        _clear_screen(game_env=game_env)

        # Check whether to keep on playing
        running = _check_inputs_from_game_step(game_env=game_env)

        # Check if we lost
        _check_if_lost(game_env=game_env)

        # Check if we win
        _check_if_win(game_env=game_env)

        # Update Worker Position
        _update_and_draw_worker_pos(game_env=game_env)
        
        # Refresh game screen
        _refresh_game(game_env, fps_controller=fps_controller, difficulty=difficulty)
