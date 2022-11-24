from src.libs import *

# =============================================================================================== #
# Color Game
# =============================================================================================== #
BLACK:pygame.Color = pygame.Color(0, 0, 0)
WHITE: pygame.Color = pygame.Color(255, 255, 255)
RED: pygame.Color = pygame.Color(255, 0, 0)
GREEN: pygame.Color = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
TAREGT_COLOR: pygame.Color = pygame.Color(0, 255, 255)


# =============================================================================================== #
# Flags Game
# =============================================================================================== #
FLAG_BLACK_BG: bool = False # Enable Black Background
NO_SEATS_FLAG: bool = False
SEATS_FLAG: bool = True

SHOW_WORKER_POS: bool = False


# =============================================================================================== #
# Constants Game
# =============================================================================================== #
# This is technically a FPS Refresh rate
# Higher number means faster refresh, thus faster Worker movement, meaning harder game play
DIFFICULTY: int = 10
WIDTH: int = 1024
HEIGHT: int = 768

RENDER_MODE: str = 'worker'


# =============================================================================================== #
# Images Game
# =============================================================================================== #
ROOT = Path(__name__).parent.parent
IMAGES = ROOT / Path("images")
BACKGROUND_IMAGE = IMAGES / Path("background.png")


# =============================================================================================== #
# Data Game
# =============================================================================================== #
if NO_SEATS_FLAG:
    SEATS_COORDS = None
    TARGET_SEAT:int = -1
    TARGET_COORDS: list = []
    TARGET_RECT = None
elif SEATS_FLAG:
    DATA = ROOT / Path("data")
    SEATS = DATA / Path("seats.pkl")
    if not FLAG_BLACK_BG:
        with open(str(SEATS), 'rb') as f:
            SEATS_COORDS = pickle.load(f)
            TARGET_SEAT:int = 10
            TARGET_COORDS: list = SEATS_COORDS[TARGET_SEAT]
            TARGET_RECT = pygame.Rect(TARGET_COORDS[0], TARGET_COORDS[1], 10, 10)
            # print(TARGET_COORDS) # [657, 702]
else:
    TARGET_COORDS: list = [500, 500]
    TARGET_RECT = pygame.Rect(TARGET_COORDS[0], TARGET_COORDS[1], 10, 10)