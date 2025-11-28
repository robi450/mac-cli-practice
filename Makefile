run:
	python main.py generate --name "Example User" --topic "Practice"

list:
	python main.py list

clean:
	rm -rf outputs/*

config:
	python main.py config --name "Demo User" --topic "Testing"

venv:
	python -m venv .venv

activate:
	source .venv/bin/activate
