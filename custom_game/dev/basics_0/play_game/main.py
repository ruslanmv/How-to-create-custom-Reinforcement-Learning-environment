from src.libs import *

from src.utils import set_seeds
from src.setup_game import setup_game
from src.play_game import play_game


def main() -> None:
    set_seeds()
    game_config = setup_game()
    play_game(game_config=game_config)


if __name__ == "__main__":
    main()
