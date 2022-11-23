from gym.envs.registration import register

register(
    id='worker-v0',
    entry_point='worker.envs:WorkerEnv',
)
