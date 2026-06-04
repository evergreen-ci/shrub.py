# Agent Guidelines

When adding a new command or making any functional change, always:

1. Bump the version in `pyproject.toml` (this project uses semantic versioning — minor bump for new features, patch for bug fixes).
2. Add a changelog entry at the top of `CHANGELOG.md` using the format:

   ```
   ## X.Y.Z - YYYY-MM-DD
   - Short description of the change.
   ```

## Project Structure

- `src/shrub/` — main package. Core types are in `command.py`, `task.py`, `variant.py`, `config.py`.
- `src/shrub/v3/` — v3 API (pydantic models for Evergreen project config objects).
- `tests/shrub/` — unit tests mirroring the `src/shrub/` layout.
- `tests/integration/` — integration tests.
- `pyproject.toml` — project metadata and dependencies (managed with Poetry).

## Running Tests

```bash
poetry run pytest
```

Tests run black formatting and mypy type checks automatically (configured in `setup.cfg`). Both must pass.

## Code Style

- Line length: 100 characters (black and flake8 are both configured to this).
- Type annotations are required; mypy runs in CI.
- New command types should follow the patterns in `src/shrub/command.py` and `src/shrub/v3/evg_command.py`.
- Use pydantic models (v2) for any new structured types in `src/shrub/v3/`.
