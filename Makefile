lint:
	black .
	flake8 .
	isort .

venv:
	python3 -m venv && python3 -m ensurepip && python3 -m pip install -r requirements.txt

run:
	sudo bash -c 'source venv/bin/activate && python3 main.py &'