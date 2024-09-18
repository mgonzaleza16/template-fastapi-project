
.PHONY: install
install: ## Install the required Python packages.
	pip install -r requirements.txt


.PHONY: run
run: ## Run the app locally.
	uvicorn app.main:app --port=8000 --reload --host=0.0.0.0


.PHONY: lint
lint: ## Run Ruff to check code quality.
	ruff check


.PHONY: format
format: ## Run Ruff to automatically fix code quality issues.
	ruff check . --fix


.PHONY: test
test: ## Run the tests against the current version of Python.
	python .\app\test\run.py
