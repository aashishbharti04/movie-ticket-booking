# Deployment Guide

CineBook ships with a production WSGI entry point (`wsgi:app`) and works on any
platform that runs Python or Docker. This guide covers the common targets.

## Production checklist

Before going live, ensure:

- [ ] `FLASK_CONFIG=production`
- [ ] A strong `SECRET_KEY` (`python -c "import secrets; print(secrets.token_hex(32))"`)
- [ ] `SESSION_COOKIE_SECURE=true` and HTTPS everywhere
- [ ] A managed database via `DATABASE_URL` (not the bundled SQLite file)
- [ ] Tables created / migrations applied (`flask db upgrade`)

> In production, the app **refuses to start** with the default `SECRET_KEY`.

## Run with a WSGI server

```bash
# Linux / macOS
gunicorn "wsgi:app" --bind 0.0.0.0:8000 --workers 3

# Windows
waitress-serve --listen=0.0.0.0:8000 wsgi:app
```

---

## Docker

A `Dockerfile` and `docker-compose.yml` are included.

```bash
# Build & run with compose (SQLite volume)
docker compose up --build
# App on http://localhost:8000
```

Or manually:

```bash
docker build -t cinebook .
docker run -p 8000:8000 \
  -e SECRET_KEY="$(python -c 'import secrets;print(secrets.token_hex(32))')" \
  -e FLASK_CONFIG=production \
  cinebook
```

---

## Render

1. New → **Web Service**, connect the repo.
2. **Build command:** `pip install -r requirements.txt`
3. **Start command:** `gunicorn "wsgi:app"`
4. Add env vars: `SECRET_KEY`, `FLASK_CONFIG=production`,
   `SESSION_COOKIE_SECURE=true`, and `DATABASE_URL` (use a Render PostgreSQL).
5. Add a build/release step to run `flask --app wsgi.py db upgrade`.

## Railway

1. **New Project → Deploy from GitHub repo.**
2. Railway autodetects Python. Set the start command to `gunicorn "wsgi:app"`.
3. Add a PostgreSQL plugin; Railway injects `DATABASE_URL`.
4. Set `SECRET_KEY`, `FLASK_CONFIG=production`, `SESSION_COOKIE_SECURE=true`.

## Fly.io

```bash
fly launch            # generates fly.toml; choose internal port 8000
fly secrets set SECRET_KEY=... FLASK_CONFIG=production SESSION_COOKIE_SECURE=true
fly deploy
```

Set the process command to `gunicorn "wsgi:app" --bind 0.0.0.0:8000`.

## Traditional VPS (systemd + Nginx)

1. Clone the repo, create a venv, `pip install -r requirements.txt gunicorn`.
2. Create a systemd unit running
   `gunicorn "wsgi:app" --bind 127.0.0.1:8000 --workers 3`.
3. Put Nginx in front for TLS termination and reverse-proxy to `127.0.0.1:8000`.
4. Store env vars in an `EnvironmentFile` (not world-readable).

---

## Using MySQL / PostgreSQL

```bash
# MySQL
pip install PyMySQL
DATABASE_URL=mysql+pymysql://user:pass@host/dbname

# PostgreSQL
pip install "psycopg[binary]"
DATABASE_URL=postgresql+psycopg://user:pass@host/dbname
```

Then run `flask --app wsgi.py db upgrade` (or `init-db` for a fresh schema).

## Health checks

Point your platform's health check at **`/healthz`** — it returns
`{"status": "ok"}` with HTTP 200.
