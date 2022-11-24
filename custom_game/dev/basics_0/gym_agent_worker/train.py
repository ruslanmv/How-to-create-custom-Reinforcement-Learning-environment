from src.libs import *
from src.setup_game import *
from src.utils import *
from src.configs import RENDER_MODE
from src.configs import WINDOW_LENGTH, IMG_SHAPE

import logging
script_name = __name__
def define_script_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    return logger
logger: logging.Logger = define_script_logger()

def main() -> None:
    logger.info(f"Setup GYM env for mode={RENDER_MODE}...")
    env = gym.make(f"{RENDER_MODE}:{RENDER_MODE}-v0")

    nb_actions = env.action_space.n
    input_shape = (WINDOW_LENGTH, IMG_SHAPE[0], IMG_SHAPE[1])
    
    logger.info(f"Create DEEP NET...")
    model: Sequential = get_model(input_shape=input_shape, nb_actions=nb_actions)
    logger.info(f"Create RL DEEP NET...")
    dqn: DQNAgent =  get_dqnagent(model=model, nb_actions=nb_actions)

    logger.info(f"FIT...")
    weights_filename = 'test_dqn_snake_weights.h5f'
    checkpoint_weights_filename = 'test_dqn_' + "snake" + '_weights_{step}.h5f'
    checkpoint_callback = ModelIntervalCheckpoint(checkpoint_weights_filename, interval=100000)
    dqn.fit(
        env,
        nb_steps=1500000,
        callbacks=[checkpoint_callback],
        log_interval=100000,
        visualize=False
    )
    logger.info(f"Save Model...")
    # After training is done, we save the final weights one more time.
    dqn.save_weights(weights_filename, overwrite=True)

    logger.info(f"Test...")
    # Load the weights
    model.load_weights("test_dqn_snake_weights.h5f")

    dqn = get_dqnagent(model=model, nb_actions=nb_actions)
    env.sleep = 0.2
    dqn.test(env, nb_episodes=1, visualize=True)
    logger.info(f"Done!")


if __name__ == "__main__":
    main()
