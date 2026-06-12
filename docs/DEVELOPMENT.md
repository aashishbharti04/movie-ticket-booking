# Development Setup Guide

This guide gets you from a fresh clone to a running, test-passing local setup.

## Prerequisites

- **Python 3.10+** (`python --version`)
- **git**
- A terminal (PowerShell, bash, zsh…)

## 1. Clone & enter

```bash
git clone https://github.com/aashishbharti04/movie-ticket-booking.git
cd movie-ticket-booking
```

## 2. Virtual environment

```bash
python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements-dev.txt   # runtime + test/lint tools
```

## 4. Environment variables

```bash
cp .env.example .env        # Windows: copy .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"   # paste into SECRET_KEY
```

## 5. Initialise the database

```bash
flask --app wsgi.py init-db     # create tables
flask --app wsgi.py seed-db     # optional demo data → demo / demopass123
```

## 6. Run the app

```bash
python run.py
# or, with auto-reload:
flask --app wsgi.py run --debug
```

Visit <http://127.0.0.1:5000>.

## Everyday commands

| Task | Command |
| --- | --- |
| Run dev server | `python run.py` |
| Run tests | `pytest` |
| Tests + coverage report | `pytest --cov=app --cov-report=term-missing` |
| Lint | `ruff check .` |
| Auto-fix lint | `ruff check --fix .` |
| Format | `ruff format .` |
| Open a shell with app context | `flask --app wsgi.py shell` |
| Regenerate screenshots | `python scripts/capture_screenshots.py` (server running) |

## Database migrations (Flask-Migrate)

```bash
flask --app wsgi.py db init          # first time only
flask --app wsgi.py db migrate -m "add column"
flask --app wsgi.py db upgrade
```

## Project layout

See [FOLDER_STRUCTURE.md](FOLDER_STRUCTURE.md) and [ARCHITECTURE.md](ARCHITECTURE.md).

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `RuntimeError: SECRET_KEY must be set…` | You're on `production` config — set a real `SECRET_KEY` or use `FLASK_CONFIG=development`. |
| `no such table` | Run `flask --app wsgi.py init-db`. |
| Want a clean slate | Delete `instance/app.db` and re-init. |
| Port 5000 busy | `flask --app wsgi.py run --port 5001`. |

## Before you open a PR

```bash
ruff check . && ruff format --check . && pytest
```

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the full workflow.
