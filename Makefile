## Targets for virtual environments

# Sets up a virtual environment and activates it
create-venv:
	pyenv local 3.11.11
	POETRY_VIRTUALENVS_IN_PROJECT=1 poetry env use $(shell pyenv which python3)
	poetry lock
	poetry install --with dev

# Activate the virtual environment
activate-venv:
	@echo "Run to activate the virtual environment: "
	@echo "source $(shell poetry env info --path)/bin/activate"

init:
	poetry run python scripts/initialize.py

## Targets for running the agent

run: 
	poetry run python scripts/run.py

run-verbose:
	poetry run python scripts/run.py --logginglevel DEBUG

test:
	poetry run pytest --cov --cov-report=term-missing --cov-report=html --disable-warnings -v
