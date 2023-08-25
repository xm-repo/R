lint:
	black .
	flake8 .
	isort .

deps:
	source venv/bin/activate && python3 -m pip install --default-timeout=100 -r requirements.txt && deactivate

run:
	sudo bash -c "source venv/bin/activate && python3 main.py &"