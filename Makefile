lint:
	black .
	flake8 .
	isort .

venv:
	python -m venv venv && python -m ensurepip && python -m pip install -r requirements.txt

run:
	sudo bash -c 'source venv/bin/activate && python main.py &'