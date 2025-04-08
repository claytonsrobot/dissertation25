install:
	poetry install
	poetry run python ./utils/update_desktop_ini.py
