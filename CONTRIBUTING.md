# Contributing to JobPlatformFastAPI

Thanks for your interest in contributing!

This project aims to be clean, production-friendly, and easy to collaborate on. Please follow the guidelines below so changes are consistent and easy to review.

---

## Quick Start

1. Fork the repo and clone your fork
2. Create a new branch
3. Make changes
4. Run formatting + lint + tests
5. Open a Pull Request

---

## Development Setup

### 1) Create a virtual environment

```bash
python -m venv env
source env/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
pip install -e ".[dev]"
pre-commit install
```

---

## Code Quality Rules

This repo uses:

- **Ruff** for linting and import sorting
- **Black** for formatting
- **Pytest** for tests
- **Pre-commit** to run checks automatically before commits

### Run checks locally

```bash
ruff check .
black --check .
pytest -q
```

### Auto-fix formatting and lint issues

```bash
ruff check . --fix
black .
```

---

## Branching

Use clear branch names:

- `feature/<short-name>`
- `fix/<short-name>`
- `chore/<short-name>`

Example:

```bash
git checkout -b feature/add-health-endpoint
```

---

## Commit Messages

Keep messages clear and scoped:

- `feat: add /health endpoint`
- `fix: handle redis startup failure`
- `chore: update dependencies`
- `docs: improve README`

---

## Pull Requests

Before opening a PR:

- Ensure CI passes
- Include a short summary of what changed
- Add screenshots or API examples if relevant
- Avoid committing secrets (never commit `.env`)

---

## Reporting Issues

If you found a bug, please include:

- steps to reproduce
- expected vs actual behavior
- logs or error traces
- OS and Python version

---

## Security

If you accidentally committed a secret:

- rotate it immediately (OpenAI, Google OAuth, etc.)
- remove it from git history if needed
- open an issue or PR explaining what was rotated

Thanks again for contributing.
