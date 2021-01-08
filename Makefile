.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: lint
lint:  ## Linter the code.
	isort simpletiming tests --check
	flake8 .
	mypy simpletiming

.PHONY: test
test:  ## Test your code.
	poetry run pytest tests/ --cov=simpletiming --cov-report=term-missing:skip-covered --cov-report=xml
