lint:
	poetry run isort .
	poetry run black .
	poetry run djlint --reformat .
	poetry run djlint --lint .
