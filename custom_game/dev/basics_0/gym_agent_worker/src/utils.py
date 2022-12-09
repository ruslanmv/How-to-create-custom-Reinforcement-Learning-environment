from src.libs import *
from src.worker_env import WorkerEnv
from src.configs import *

# =============================================================================================== #
# Utils
# =============================================================================================== #

def set_seeds():
    random.seed(SEED)
    np.random.seed(SEED)


class ImageProcessor(Processor):
    def process_observation(self, observation):
        # First convert the numpy array to a PIL Image
        img = Image.fromarray(observation)
        # Then resize the image
        img = img.resize(IMG_SHAPE)
        # And convert it to grayscale  (The L stands for luminance)
        img = img.convert("L")
        # Convert the image back to a numpy array and finally return the image
        img = np.array(img)
        return img.astype('uint8')  # saves storage in experience memory
    
    def process_state_batch(self, batch):

        # We divide the observations by 255 to compress it into the intervall [0, 1].
        # This supports the training of the network
        # We perform this operation here to save memory.
        processed_batch = batch.astype('float32') / 255.
        return processed_batch

    def process_reward(self, reward):
        return np.clip(reward, -1., 1.)


def get_model(input_shape, nb_actions) -> Sequential:
    """Get tf-keras sequential model."""

    model: Sequential = Sequential()
    model.add(Permute((2, 3, 1), input_shape=input_shape))

    model.add(Convolution2D(32, (8, 8), strides=(4, 4),kernel_initializer='he_normal'))
    model.add(Activation('relu'))
    model.add(Convolution2D(64, (4, 4), strides=(2, 2), kernel_initializer='he_normal'))
    model.add(Activation('relu'))
    model.add(Convolution2D(64, (3, 3), strides=(1, 1), kernel_initializer='he_normal'))
    model.add(Activation('relu'))
    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dense(nb_actions))
    model.add(Activation('linear'))
    print(model.summary())
    return model


def get_dqnagent(model, nb_actions) -> DQNAgent:
    """Get tf-keras-rl model."""
    
    processor = ImageProcessor()
    memory = SequentialMemory(limit=1000000, window_length=WINDOW_LENGTH)
    policy = LinearAnnealedPolicy(
        EpsGreedyQPolicy(),
        attr='eps',
        value_max=1.,
        value_min=.1,
        value_test=.05,
        nb_steps=1000000
    )
    dqn: DQNAgent = DQNAgent(
        model=model,
        nb_actions=nb_actions,
        policy=policy,
        memory=memory,
        processor=processor,
        nb_steps_warmup=50000, 
        gamma=.99,
        target_model_update=10000,
        train_interval=4, delta_clip=1
    )
    dqn.compile(Adam(learning_rate=.00025), metrics=['mae'])
    return dqn
