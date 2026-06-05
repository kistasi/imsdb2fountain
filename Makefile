-include .env
export

.DEFAULT_GOAL := run

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

$(VENV)/.installed: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install --quiet -r requirements.txt
	touch $@

run: $(VENV)/.installed
	$(PYTHON) src/main.py

clean:
	find downloaded-scripts -type f -delete
	rm -rf output
