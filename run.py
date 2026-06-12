"""Convenience launcher for local development.

    python run.py

Prefer ``flask run`` during day-to-day development; this script exists so the
app can be started with a bare ``python run.py`` on any platform.
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=app.config.get("DEBUG", False))
