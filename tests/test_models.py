"""Unit tests for the ORM models."""

from app.models import Booking, User


def test_password_is_hashed_not_plaintext(app):
    u = User(
        username="bob",
        email="b@x.com",
        first_name="Bob",
        last_name="Lee",
        phone="123456789",
    )
    u.set_password("plaintext-secret")
    assert u.password_hash != "plaintext-secret"
    assert u.check_password("plaintext-secret")
    assert not u.check_password("wrong")


def test_full_name(app):
    u = User(first_name="Ada", last_name="Lovelace")
    assert u.full_name == "Ada Lovelace"


def test_booking_total_price(app):
    b = Booking(seat_class="AC Premium", seats=3)
    assert b.unit_price == 350
    assert b.compute_total() == 1050
