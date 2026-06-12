# Architecture

CineBook is a server-rendered Flask application built around the
**application-factory** pattern and **blueprints**. It favours simplicity,
testability and security over framework magic.

## High-level overview

```
                         ┌─────────────────────────────┐
   Browser  ──HTTP(S)──▶ │          Flask app          │
   (Jinja2 +            │  create_app() factory        │
    CSS + JS)           │                              │
                        │  ┌────────── Blueprints ────┐ │
                        │  │ main · auth · bookings   │ │
                        │  └──────────────────────────┘ │
                        │  Flask-WTF (CSRF, forms)      │
                        │  Flask-Login (sessions)       │
                        │  SQLAlchemy ORM ──────────────┼──▶  Database
                        └─────────────────────────────┘     (SQLite / MySQL /
                                                              PostgreSQL)
```

## Request lifecycle

1. A request hits a **blueprint route** (`app/blueprints/*.py`).
2. For form submissions, a **WTForms** form validates and sanitises input
   (CSRF token checked automatically).
3. The route uses the **SQLAlchemy ORM** (`app/models.py`) to read/write data —
   never raw SQL.
4. A **Jinja2 template** (`app/templates/`) renders the response, extending
   `base.html` and reusing components/macros.
5. **Flask-Login** attaches the current user to each request and guards
   protected views with `@login_required`.

## Key design decisions

| Decision | Rationale |
| --- | --- |
| **Application factory** (`create_app`) | Enables isolated app instances per test/config; avoids import-time side effects. |
| **Blueprints** | Each feature area (auth, bookings, public) is self-contained and independently testable. |
| **Extensions in `extensions.py`** | Singletons live in one module so models and blueprints import them without circular dependencies. |
| **Config classes from env** | `development` / `testing` / `production` profiles; secrets never hardcoded. Production refuses the default `SECRET_KEY`. |
| **ORM-only data access** | Eliminates the SQL-injection class of bugs entirely. |
| **Server-rendered + vanilla JS** | No build step, tiny payload, great Lighthouse scores, progressive enhancement. |
| **CSS design tokens** | Theming (dark/light) and consistency through CSS custom properties — no framework lock-in. |

## Data model

```
┌────────────────┐         ┌──────────────────────┐
│      User      │ 1     * │       Booking        │
├────────────────┤◀────────├──────────────────────┤
│ id (PK)        │         │ id (PK)              │
│ username (UQ)  │         │ user_id (FK)         │
│ email (UQ)     │         │ movie_name           │
│ first_name     │         │ seat_class (enum)    │
│ last_name      │         │ seats                │
│ phone          │         │ show_time            │
│ password_hash  │         │ snacks (nullable)    │
│ created_at     │         │ total_price          │
└────────────────┘         │ status               │
                           │ created_at           │
                           └──────────────────────┘
```

- One `User` has many `Booking`s (`cascade="all, delete-orphan"`).
- `seat_class` is constrained to a known set; pricing is derived from
  `SEAT_PRICES` in `app/models.py`.

## Security layers

See [SECURITY.md](../SECURITY.md) for the full list — ORM, password hashing,
CSRF, validation, hardened cookies, open-redirect protection and per-user
authorization checks.

## Extensibility

- **Add a feature area** → create a new blueprint under `app/blueprints/` and
  register it in `app/__init__.py`.
- **Add a model** → define it in `app/models.py`, then
  `flask db migrate -m "..."` and `flask db upgrade`.
- **Swap the database** → set `DATABASE_URL`; no code changes required.
