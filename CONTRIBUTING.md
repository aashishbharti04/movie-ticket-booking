# Contributing to CineBook

First off — thank you for taking the time to contribute! 🎉
This guide will help you get a productive development environment running and
explain how we work.

## Code of Conduct

This project is governed by our [Code of Conduct](CODE_OF_CONDUCT.md).
By participating, you are expected to uphold it.

## Getting Started

1. **Fork** the repository and clone your fork.
2. Set up the environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
   pip install -r requirements-dev.txt
   cp .env.example .env
   flask --app wsgi.py init-db
   ```
3. Run the app: `python run.py` → <http://127.0.0.1:5000>

See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for a deeper walkthrough.

## Development Workflow

1. Create a branch from `main`:
   ```bash
   git checkout -b feat/short-description
   ```
   Use a prefix: `feat/`, `fix/`, `docs/`, `refactor/`, `test/`, `chore/`.
2. Make your change with clear, focused commits.
3. **Run the checks locally before pushing:**
   ```bash
   ruff check .          # lint
   ruff format .         # format
   pytest                # tests + coverage
   ```
4. Push and open a Pull Request against `main`, filling in the PR template.

## Commit Messages

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add seat availability indicator
fix: prevent negative seat counts
docs: clarify deployment steps
```

## Coding Standards

- **Python**: formatted and linted with [ruff](https://github.com/astral-sh/ruff)
  (config in `pyproject.toml`). Line length 88.
- **Type hints** where they add clarity; `from __future__ import annotations` at
  the top of modules.
- **Tests**: every new feature or bug fix should come with a test. Keep coverage
  from regressing.
- **Templates/CSS**: reuse the existing design tokens and components; avoid
  inline styles where a class exists.
- Never commit secrets, `.env` files or the `instance/` folder.

## Reporting Bugs & Requesting Features

Use the issue templates:
- 🐞 [Bug report](.github/ISSUE_TEMPLATE/bug_report.md)
- ✨ [Feature request](.github/ISSUE_TEMPLATE/feature_request.md)

For security vulnerabilities, **do not open a public issue** — follow
[SECURITY.md](SECURITY.md).

## Pull Request Checklist

- [ ] Tests pass (`pytest`) and lint is clean (`ruff check .`).
- [ ] New behaviour is covered by tests.
- [ ] Docs/README updated if behaviour changed.
- [ ] No secrets or generated files committed.

Thanks again for helping make CineBook better! 💜
