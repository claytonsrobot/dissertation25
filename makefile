install:
	poetry install
	poetry run python -m utils.post_clone_update_desktop_ini_ico_paths
