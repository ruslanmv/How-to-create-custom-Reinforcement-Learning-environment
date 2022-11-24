MAIN_SCRIPT = main.py
CREATE_GYM_ENV = create_gym_env.py
PY_INTERPRETER = python3
PIP = pip3
ENV_NAME = worker

# exce as: make -f Makefile play_game
play_game: clear_screen
	$(PY_INTERPRETER) $(MAIN_SCRIPT)

# exce as: make -f Makefile create_gym_env
create_gym_env: install_gym_env
	$(PY_INTERPRETER) $(CREATE_GYM_ENV)

# exce as: make -f Makefile install_gym_env
install_gym_env: clear_gym_cache
	$(PIP) install -e $(ENV_NAME)

# exce as: make -f Makefile clear_gym_cache
clear_gym_cache: clear_screen
	rm -rf $(ENV_NAME)/gym$(ENV_NAME).egg-info
	rm -rf $(ENV_NAME)/$(ENV_NAME)/__pycache__
	rm -rf $(ENV_NAME)/$(ENV_NAME)/envs/__pycache__
	rm -rf $(ENV_NAME)/$(ENV_NAME)/envs/src/__pycache__

clear_screen:
	clear
