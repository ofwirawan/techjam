help:
	@echo "Targets: install, run, test, fmt"

install:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

run:
	uvicorn app.main:app --reload --port 8000

test:
	pytest -q

fmt:
	python -m pip install ruff && ruff check . --fix
