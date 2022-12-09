from src.libs import *

# =============================================================================================== #
# Color Game
# =============================================================================================== #
BLACK:pygame.Color = pygame.Color(0, 0, 0)
WHITE: pygame.Color = pygame.Color(255, 255, 255)
RED: pygame.Color = pygame.Color(255, 0, 0)
GREEN: pygame.Color = pygame.Color(0, 255, 0)
BLUE: pygame.Color = pygame.Color(0, 0, 255)
TAREGT_COLOR: pygame.Color = pygame.Color(255,215,0)# pygame.Color(0, 255, 255)


# =============================================================================================== #
# Flags Game
# =============================================================================================== #
FLAG_BLACK_BG: bool = False # Enable Black Background
NO_SEATS_FLAG: bool = False
SEATS_FLAG: bool = True
STEPS: int = 1000

SHOW_WORKER_POS: bool = False
RANDOM_SEAT: bool = True

# =============================================================================================== #
# Constants Game
# =============================================================================================== #
# This is technically a FPS Refresh rate
# Higher number means faster refresh, thus faster Worker movement, meaning harder game play
DIFFICULTY: int = 10
WIDTH: int = 1024 # 1024
HEIGHT: int = 768 # 768

RENDER_MODE: str = 'worker'
TARGET_SEAT:int = 50

SEED = 1234


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
    CLUSTERS = DATA / Path("clusters.csv")
    
    if not FLAG_BLACK_BG:
        with open(str(SEATS), 'rb') as f:
            SEATS_COORDS = pickle.load(f)
        SEATS_CLUSTERS = pd.read_csv(str(CLUSTERS))
        SEATS_CLUSTERS["occupied"] = [random.randint(0, 1) for _ in range(SEATS_CLUSTERS.shape[0])]
        if RANDOM_SEAT:
            TARGET_SEAT = random.randint(0, len(SEATS_COORDS))
        TARGET_COORDS: list = SEATS_COORDS[TARGET_SEAT]
        TARGET_RECT = pygame.Rect(TARGET_COORDS[0], TARGET_COORDS[1], 10, 10)
        # print(TARGET_COORDS) # [657, 702]
else:
    TARGET_COORDS: list = [500, 500]
    TARGET_RECT = pygame.Rect(TARGET_COORDS[0], TARGET_COORDS[1], 10, 10)
