MAIN_SCRIPT = main.py
SCRIPTS = scripts
SHOW_BLURRED_IMAGE = $(SCRIPTS)/"show_blurred_image.py"
FIND_CONTOURS = $(SCRIPTS)/"find_contours.py"
PY_INTERPRETER = python3

# make -f Makefile run_main
run_main: clear_screen
	$(PY_INTERPRETER) $(MAIN_SCRIPT)

# make -f Makefile show_blurred_image_to_main
show_blurred_image_to_main: clear_screen
	ln -sfn $(SHOW_BLURRED_IMAGE) $(MAIN_SCRIPT)

# make -f Makefile find_contours_to_main
find_contours_to_main: clear_screen
	ln -sfn $(FIND_CONTOURS) $(MAIN_SCRIPT)

activate_env: clear_screen
	source ~/anaconda3/bin/activate && conda activate data_game_env

clear_screen:
	clear
