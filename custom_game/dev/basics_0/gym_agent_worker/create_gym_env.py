import time
import matplotlib.pyplot as plt
import gym
from src.configs import RENDER_MODE

def main():
    # env = gym.make(f"{RENDER_MODE}:{RENDER_MODE}-v0")
    env = gym.make(f"worker:worker-v0")

    env.reset()
    env.render(f"human")
    action = env.action_space.sample()
    img, reward, done, info = env.step(1)
    print(reward, done, info)
    plt.figure()
    plt.imshow(img)
    plt.show()

    env.reset()
    for i in range(100):
        env.render(f"{RENDER_MODE}")
        action = env.action_space.sample()
        img, reward, done, info = env.step(action)
        time.sleep(0.1)


if __name__ == "__main__":
    main()