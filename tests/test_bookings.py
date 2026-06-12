"""Tests for the booking dashboard and access scoping."""

from datetime import datetime, timedelta, timezone

from app.models import Booking, User


def _future_show_time() -> str:
    return (datetime.now(timezone.utc) + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M")


def test_create_booking(auth_client, db):
    resp = auth_client.post(
        "/dashboard/new",
        data={
            "movie_name": "Interstellar",
            "seat_class": "AC Premium",
            "seats": 2,
            "show_time": _future_show_time(),
            "snacks": "Popcorn",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200
    booking = Booking.query.filter_by(movie_name="Interstellar").first()
    assert booking is not None
    assert booking.total_price == 700  # 350 * 2


def test_create_booking_rejects_zero_seats(auth_client):
    resp = auth_client.post(
        "/dashboard/new",
        data={
            "movie_name": "X",
            "seat_class": "AC Premium",
            "seats": 0,
            "show_time": _future_show_time(),
        },
    )
    assert resp.status_code == 200
    assert Booking.query.filter_by(movie_name="X").first() is None


def test_user_cannot_cancel_others_booking(auth_client, db):
    # Booking owned by a different user
    other = User(
        username="mallory",
        email="m@x.com",
        first_name="Mal",
        last_name="Ory",
        phone="123456789",
    )
    other.set_password("password123")
    db.session.add(other)
    db.session.flush()
    booking = Booking(
        user_id=other.id,
        movie_name="Secret",
        seat_class="First Class",
        seats=1,
        show_time=datetime.now(timezone.utc) + timedelta(days=1),
        total_price=180,
    )
    db.session.add(booking)
    db.session.commit()

    resp = auth_client.post(f"/dashboard/{booking.id}/cancel")
    assert resp.status_code == 403
    # Booking still exists
    assert Booking.query.get(booking.id) is not None
