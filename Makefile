lint:
	black --line-length=100 .
	flake8 .
	isort .

deps:
	source venv/bin/activate && python3 -m pip install --default-timeout=100 -r requirements.txt && deactivate

local:
	PORT=80 USE_SSL='' python3 main.py

run:
	sudo bash -c "source venv/bin/activate && python3 main.py &"