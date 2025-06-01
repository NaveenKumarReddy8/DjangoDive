lint:
	uv run ruff format .
	uv run djlint --reformat .
	uv run djlint --lint .

server:
	uv run python manage.py runserver