"""Database models.

The original script stored everything in a single flat ``theatre`` table
with plaintext passwords and SQL built via string formatting. Here the data
is normalised into ``User`` and ``Booking`` tables, passwords are hashed, and
all access goes through the SQLAlchemy ORM (no hand-built SQL, no injection).
"""

from __future__ import annotations

from datetime import datetime, timezone

from flask_login import UserMixin
from sqlalchemy import Enum as SAEnum
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


# Seat classes preserve the original "AC / Non-AC / 1st / 2nd class" concepts.
SEAT_CLASSES = ("AC Premium", "AC Balcony", "First Class", "Second Class")
SEAT_PRICES = {
    "AC Premium": 350,
    "AC Balcony": 280,
    "First Class": 180,
    "Second Class": 120,
}


class User(UserMixin, db.Model):
    """An authenticated customer who can book tickets."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=_utcnow, nullable=False)

    bookings = db.relationship(
        "Booking",
        back_populates="user",
        cascade="all, delete-orphan",
        order_by="Booking.created_at.desc()",
    )

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<User {self.username}>"


class Booking(db.Model):
    """A single ticket booking made by a user."""

    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    movie_name = db.Column(db.String(120), nullable=False)
    seat_class = db.Column(SAEnum(*SEAT_CLASSES, name="seat_class"), nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    show_time = db.Column(db.DateTime(timezone=True), nullable=False)
    snacks = db.Column(db.String(200), nullable=True)
    total_price = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default="confirmed")
    created_at = db.Column(db.DateTime(timezone=True), default=_utcnow, nullable=False)

    user = db.relationship("User", back_populates="bookings")

    @property
    def unit_price(self) -> int:
        return SEAT_PRICES.get(self.seat_class, 0)

    def compute_total(self) -> int:
        return self.unit_price * (self.seats or 0)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Booking {self.movie_name} x{self.seats}>"
