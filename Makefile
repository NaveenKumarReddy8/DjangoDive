lint:
	uv run ruff format .
	uv run djlint --reformat .
	uv run djlint --lint .