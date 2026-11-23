# Repository guide

## Project layout

- `tna_utilities/` contains the public Python utilities. Flask and Django integrations live in `tna_utilities/flask/` and `tna_utilities/django/`.
- `tests/` contains `unittest` tests, generally grouped by module.
- `docs/` contains the MkDocs documentation; `docs/index.md` links to the individual pages. `CHANGELOG.md` uses Keep a Changelog and Semantic Versioning.
- `pyproject.toml` and `poetry.lock` define packaging and dependencies.

## Development

- Python 3.11 and later are supported. CI tests Python 3.11-3.15 on Linux, macOS and Windows.
- `requests` is a runtime dependency; Flask and Django are optional extras. Django 6 requires Python 3.12 or later. Django tests skip when Django 6 is unavailable.
- Preserve existing public APIs and optional-dependency boundaries. When changing behavior, update the relevant tests and documentation; record user-facing changes under `Unreleased` in `CHANGELOG.md`.
- Follow existing type annotations and formatting. Tests use `unittest`, and API tests mock HTTP calls rather than contacting a real service.

## Commands

Run from the repository root:

```sh
# Install test dependencies with Poetry and run the complete test suite
bash ./tasks/test.sh

# Run one test file using an environment with its dependencies installed
python3 -m unittest discover -s tests -p 'test_currency.py'

# Check or apply formatting (requires Docker)
bash ./tasks/checkformat.sh
bash ./tasks/format.sh

# Build the distribution with Poetry
bash ./tasks/build.sh
```

The formatting scripts use the `ghcr.io/nationalarchives/tna-python-dev:preview` image. The repository's `ruff.toml` extends a configuration inside that image, so a standalone local Ruff invocation may not find the base configuration.

## Documentation deployment

`mkdocs.yml` configures the documentation site. On pushes to `main` affecting the docs, MkDocs configuration or deployment workflow, GitHub Actions builds the site with the MkDocs Material Docker image and deploys it to GitHub Pages.
