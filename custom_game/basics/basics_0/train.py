from src.libs import *
from src.setup_game import *
from src.utils import *

IMG_SHAPE = (84, 84)
WINDOW_LENGTH = 4


def main() -> None:
    env = gym.make("{RENDER_MODE}:{RENDER_MODE}-v0")
    nb_actions = env.action_space.n

    input_shape = (WINDOW_LENGTH, IMG_SHAPE[0], IMG_SHAPE[1])
    model: Sequential = get_model(input_shape=input_shape)
    dqn: DQNAgent =  get_dqnagent(model=model)

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

    # After training is done, we save the final weights one more time.
    dqn.save_weights(weights_filename, overwrite=True)

    # Load the weights
    model.load_weights("test_dqn_snake_weights.h5f")

    dqn = get_dqnagent(model=model)
    env.sleep = 0.2
    dqn.test(env, nb_episodes=1, visualize=True)


if __name__ == "__main__":
    main()
