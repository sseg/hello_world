run_dev:
	gunicorn --reload -c config/gunicorn.py http_agent.app:application config/app.yaml

types:
	mypy --fast-parser --silent-imports --python-version 3.6 .

flake:
	python -m flake8

checks: types flake

tests:
	py.test
