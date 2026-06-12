# Folder Structure

```
movie-ticket-booking/
│
├── app/                          # Application package
│   ├── __init__.py               # create_app() factory, error handlers, context
│   ├── config.py                 # Env-driven config classes (dev/test/prod)
│   ├── extensions.py             # Extension singletons (db, login, csrf, migrate)
│   ├── models.py                 # SQLAlchemy models: User, Booking
│   ├── forms.py                  # WTForms with server-side validation
│   ├── cli.py                    # `flask init-db` / `flask seed-db`
│   │
│   ├── blueprints/               # Feature areas (each self-contained)
│   │   ├── main.py               # Landing, about, health check
│   │   ├── auth.py               # Signup, login, logout
│   │   └── bookings.py           # Dashboard, create, cancel
│   │
│   ├── templates/                # Jinja2 templates
│   │   ├── base.html             # Layout: nav, theme toggle, flashes, footer
│   │   ├── components/           # Reusable partials & macros
│   │   │   ├── footer.html
│   │   │   └── forms.html        # render_field() macro
│   │   ├── main/                 # index.html, about.html
│   │   ├── auth/                 # login.html, signup.html
│   │   ├── bookings/             # dashboard.html, create.html
│   │   └── errors/               # 403.html, 404.html, 500.html
│   │
│   └── static/                   # Front-end assets (no build step)
│       ├── css/styles.css        # Design system (tokens, components, themes)
│       ├── js/app.js             # Theme, nav, flashes, loading states
│       └── img/favicon.svg
│
├── tests/                        # pytest suite
│   ├── conftest.py               # Fixtures: app, client, user, auth_client
│   ├── test_models.py
│   ├── test_auth.py
│   └── test_bookings.py
│
├── docs/                         # Documentation
│   ├── ARCHITECTURE.md
│   ├── FOLDER_STRUCTURE.md
│   ├── API.md
│   ├── DEPLOYMENT.md
│   ├── DEVELOPMENT.md
│   ├── screenshots/              # README screenshots
│   └── report/                   # Original project report & presentation
│
├── scripts/
│   └── capture_screenshots.py    # Playwright screenshot generator
│
├── legacy/                       # Original CLI script (reference only)
│   ├── source_code.py
│   └── README.md
│
├── .github/
│   ├── workflows/                # ci.yml, codeql.yml
│   ├── ISSUE_TEMPLATE/           # bug_report, feature_request, config
│   └── PULL_REQUEST_TEMPLATE.md
│
├── instance/                     # (gitignored) SQLite DB, logs — created at runtime
│
├── wsgi.py                       # Production entry point (gunicorn/waitress)
├── run.py                        # Local dev launcher
├── requirements.txt              # Runtime dependencies
├── requirements-dev.txt          # Dev/test/CI dependencies
├── pyproject.toml                # ruff + pytest config, project metadata
├── Dockerfile                    # Container image
├── docker-compose.yml            # Local container orchestration
├── .env.example                  # Sample environment configuration
├── .gitignore
│
├── README.md
├── LICENSE                       # MIT
├── CONTRIBUTING.md
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
└── SECURITY.md
```

## Conventions

- **One blueprint per feature area.** Routes stay thin; logic lives in models.
- **Templates mirror blueprints** (`templates/<blueprint>/<view>.html`).
- **Shared UI** goes in `templates/components/` as includes or macros.
- **Nothing runtime-generated is committed** — `instance/`, `*.db`, `.env`,
  coverage and caches are all gitignored.
