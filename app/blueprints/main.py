"""Public-facing pages: landing page and static info."""

from __future__ import annotations

from flask import Blueprint, render_template
from flask_login import current_user

from ..models import SEAT_CLASSES, SEAT_PRICES

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    seat_tiers = [{"name": name, "price": SEAT_PRICES[name]} for name in SEAT_CLASSES]
    return render_template("main/index.html", seat_tiers=seat_tiers, user=current_user)


@main_bp.route("/about")
def about():
    return render_template("main/about.html")


@main_bp.route("/healthz")
def healthz():
    """Lightweight health-check endpoint for uptime monitors / CI."""
    return {"status": "ok"}, 200
