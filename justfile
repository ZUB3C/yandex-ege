lint:
    uv run ruff check --fix
    uv run ruff format

typing:
    uv run basedpyright
