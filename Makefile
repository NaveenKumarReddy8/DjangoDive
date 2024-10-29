lint:
	poetry run ruff check --fix .
	poetry run ruff format .
	poetry run djlint --lint .
	poetry run djlint --reformat .

server:
	poetry run python manage.py runserver