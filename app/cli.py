"""Custom Flask CLI commands for database setup and demo seeding."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import click
from flask import Flask

from .extensions import db
from .models import Booking, User


def register_cli(app: Flask) -> None:
    @app.cli.command("init-db")
    def init_db() -> None:
        """Create all database tables."""
        db.create_all()
        click.secho("Database tables created.", fg="green")

    @app.cli.command("seed-db")
    def seed_db() -> None:
        """Populate the database with a demo user and bookings."""
        db.create_all()
        if User.query.filter_by(username="demo").first():
            click.secho("Demo data already present.", fg="yellow")
            return

        demo = User(
            username="demo",
            email="demo@example.com",
            first_name="Demo",
            last_name="User",
            phone="+1 555 0100",
        )
        demo.set_password("demopass123")
        db.session.add(demo)
        db.session.flush()

        now = datetime.now(timezone.utc)
        samples = [
            ("Interstellar", "AC Premium", 2, now + timedelta(days=1)),
            ("Inception", "First Class", 3, now + timedelta(days=2)),
            ("Dune: Part Two", "AC Balcony", 4, now + timedelta(days=3)),
        ]
        for movie, seat_class, seats, show_time in samples:
            booking = Booking(
                user_id=demo.id,
                movie_name=movie,
                seat_class=seat_class,
                seats=seats,
                show_time=show_time,
                snacks="Popcorn & Cola",
            )
            booking.total_price = booking.compute_total()
            db.session.add(booking)

        db.session.commit()
        click.secho("Seeded demo user (login: demo / demopass123).", fg="green")
