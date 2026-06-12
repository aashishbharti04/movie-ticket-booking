"""Application factory for the Movie Ticket Booking platform.

This module wires together configuration, extensions, blueprints, CLI
commands and error handlers. The factory pattern keeps the app importable
for tests and lets us spin up isolated instances with different configs.
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from flask import Flask, render_template

from .config import config_by_name
from .extensions import csrf, db, login_manager, migrate


def create_app(config_name: str | None = None) -> Flask:
    """Create and configure a Flask application instance.

    Args:
        config_name: One of ``development``, ``testing`` or ``production``.
            Falls back to the ``FLASK_CONFIG`` env var, then ``development``.
    """
    app = Flask(__name__, instance_relative_config=True)

    config_class = config_by_name(config_name)
    app.config.from_object(config_class)
    config_class.init_app(app)

    _ensure_instance_folder(app)
    _register_extensions(app)
    _register_blueprints(app)
    _register_error_handlers(app)
    _register_cli(app)
    _register_shell_context(app)
    _register_context_processors(app)
    _configure_logging(app)

    return app


def _register_context_processors(app: Flask) -> None:
    from datetime import datetime, timezone

    @app.context_processor
    def inject_globals() -> dict:
        return {"now_year": datetime.now(timezone.utc).year}


def _ensure_instance_folder(app: Flask) -> None:
    """Create the instance folder so SQLite/uploads have a home."""
    try:
        Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    except OSError:  # pragma: no cover - defensive
        app.logger.warning("Could not create instance path: %s", app.instance_path)


def _register_extensions(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please sign in to access this page."
    login_manager.login_message_category = "warning"

    from .models import User  # local import to avoid circular dependency

    @login_manager.user_loader
    def load_user(user_id: str) -> User | None:
        return db.session.get(User, int(user_id))


def _register_blueprints(app: Flask) -> None:
    from .blueprints.auth import auth_bp
    from .blueprints.bookings import bookings_bp
    from .blueprints.main import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(bookings_bp)


def _register_error_handlers(app: Flask) -> None:
    @app.errorhandler(403)
    def forbidden(error):  # noqa: ANN001
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(error):  # noqa: ANN001
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(error):  # noqa: ANN001
        db.session.rollback()
        return render_template("errors/500.html"), 500


def _register_cli(app: Flask) -> None:
    from .cli import register_cli

    register_cli(app)


def _register_shell_context(app: Flask) -> None:
    from .models import Booking, User

    @app.shell_context_processor
    def make_shell_context() -> dict:
        return {"db": db, "User": User, "Booking": Booking}


def _configure_logging(app: Flask) -> None:
    if app.debug or app.testing:
        return
    logs_dir = Path(app.instance_path) / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(
        logs_dir / "app.log", maxBytes=1_000_000, backupCount=5
    )
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Movie Ticket Booking startup")
