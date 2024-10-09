## How to run project
### Install poetry: 
`pipx install poetry`
### Install project dependencies
`poetry install`
### Activate poetry shell
`poetry shell`
### Run server
`poetry run uvicorn app.main:app --reload`
### Run tests
`poetry run pytest`

## Code formatting tools:
Formatting config is provided in editorconfig file
## Type checking
Type checking is performed with mypy: `poetry run mypy`
## Linter
Linting is performed with pylint: ` poetry run pylint app/`