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

daemon: $(VENV)/.installed
	nohup $(PYTHON) src/main.py > pipeline.log 2>&1 & echo $$! > pipeline.pid
	@echo "Started (pid $$(cat pipeline.pid)). Logs: tail -f pipeline.log"

log:
	tail -f pipeline.log

stop:
	@if [ -f pipeline.pid ]; then \
		kill $$(cat pipeline.pid) && rm pipeline.pid && echo "Stopped."; \
	else \
		echo "No pipeline.pid found."; \
	fi

clean:
	find downloaded-scripts -type f -delete
	rm -rf output
