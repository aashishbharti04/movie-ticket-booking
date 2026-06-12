"""Tests for signup, login, logout and access control."""

from app.models import User


def test_index_loads(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Movie tickets" in resp.data


def test_healthz(client):
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_signup_creates_user(client, db):
    resp = client.post(
        "/auth/signup",
        data={
            "first_name": "Carol",
            "last_name": "King",
            "username": "carol",
            "email": "carol@example.com",
            "phone": "+1 555 0199",
            "password": "password123",
            "confirm": "password123",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert User.query.filter_by(username="carol").first() is not None


def test_signup_rejects_mismatched_passwords(client):
    resp = client.post(
        "/auth/signup",
        data={
            "first_name": "Dan",
            "last_name": "Bo",
            "username": "dan",
            "email": "dan@example.com",
            "phone": "123456789",
            "password": "password123",
            "confirm": "different123",
        },
    )
    assert resp.status_code == 200
    assert b"Passwords must match" in resp.data


def test_login_success(client, user):
    resp = client.post(
        "/auth/login",
        data={"identifier": "alice", "password": "supersecret1"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"Welcome back" in resp.data


def test_login_invalid_credentials(client, user):
    resp = client.post(
        "/auth/login",
        data={"identifier": "alice", "password": "wrongpass"},
    )
    assert resp.status_code == 401
    assert b"Invalid credentials" in resp.data


def test_dashboard_requires_login(client):
    resp = client.get("/dashboard/", follow_redirects=False)
    assert resp.status_code == 302
    assert "/auth/login" in resp.headers["Location"]
