# Contributing

Thanks for helping improve MaintainerLens.

## Before opening a pull request

1. Open an issue describing the bug or proposed change.
2. Keep pull requests focused and explain the user-visible impact.
3. Add or update tests for changed core behaviour.
4. Update the README or architecture notes when setup, configuration, or behaviour changes.
5. Do not commit API tokens, credentials, private issue data, or local environment files.

## Local checks

```bash
python -m pip install -r requirements-dev.txt
python -m compileall -q maintainerlens tests streamlit_app.py
ruff check maintainerlens tests
ruff format --check maintainerlens tests
pytest
```

All checks should pass before requesting review.
