# Changelog

All notable changes to this project are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.0.0] — 2026-06-12

The first stable release: a complete rebuild of the original command-line
script into a secure, production-ready Flask web application.

### Added
- Flask application using the application-factory pattern and blueprints
  (`auth`, `bookings`, `main`).
- User registration, login and logout with Flask-Login sessions.
- Booking dashboard: create, list (paginated), cancel, and per-user stats.
- Seat classes with per-seat pricing and automatic total calculation.
- Responsive, accessible UI with a custom CSS design system.
- Dark and light themes with system detection and persistence.
- Loading, skeleton, empty and error (403/404/500) states.
- SQLAlchemy models with database-agnostic configuration (SQLite default).
- Flask-Migrate (Alembic) integration for schema migrations.
- CLI commands: `init-db` and `seed-db`.
- Test suite with pytest + coverage, and ruff linting.
- GitHub Actions CI (lint, test, build verification).
- Full documentation set (architecture, folder structure, API, deployment,
  development) and screenshots.
- Open-source scaffolding: README, LICENSE (MIT), CONTRIBUTING,
  CODE_OF_CONDUCT, SECURITY, issue/PR templates.

### Security
- Replaced string-formatted SQL with the SQLAlchemy ORM (eliminates SQL injection).
- Replaced plaintext passwords with salted PBKDF2 hashes.
- Moved hardcoded database credentials to environment variables.
- Added CSRF protection, server-side input validation, hardened session cookies
  and open-redirect protection on login.

### Changed
- Original CLI script preserved unchanged in `legacy/` for reference.

[1.0.0]: https://github.com/aashishbharti04/movie-ticket-booking/releases/tag/v1.0.0
