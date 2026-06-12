"""Authentication: signup, login and logout.

Passwords are hashed with Werkzeug's PBKDF2 implementation and sessions are
managed by Flask-Login. Open-redirect attacks on the ``next`` parameter are
blocked by validating the target is a local URL.
"""

from __future__ import annotations

from urllib.parse import urlparse

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user

from ..extensions import db
from ..forms import LoginForm, SignupForm
from ..models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def _is_safe_url(target: str | None) -> bool:
    """Only allow redirects to relative paths on this host."""
    if not target:
        return False
    parsed = urlparse(target)
    return parsed.netloc == "" and parsed.scheme == "" and target.startswith("/")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("bookings.dashboard"))

    form = SignupForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower(),
            first_name=form.first_name.data.strip(),
            last_name=form.last_name.data.strip(),
            phone=form.phone.data.strip(),
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Welcome aboard! Your account is ready.", "success")
        return redirect(url_for("bookings.dashboard"))

    return render_template("auth/signup.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("bookings.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        identifier = form.identifier.data.strip()
        user = User.query.filter(
            (User.username == identifier) | (User.email == identifier.lower())
        ).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid credentials. Please try again.", "danger")
            return render_template("auth/login.html", form=form), 401

        login_user(user, remember=True)
        flash(f"Welcome back, {user.first_name}!", "success")
        next_url = request.args.get("next")
        if _is_safe_url(next_url):
            return redirect(next_url)
        return redirect(url_for("bookings.dashboard"))

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("You have been signed out.", "info")
    return redirect(url_for("main.index"))
