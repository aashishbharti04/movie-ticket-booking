"""Shared pytest fixtures."""

from __future__ import annotations

import pytest

from app import create_app
from app.extensions import db as _db
from app.models import User


@pytest.fixture()
def app():
    app = create_app("testing")
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def db(app):
    return _db


@pytest.fixture()
def user(app):
    """A persisted user with a known password."""
    u = User(
        username="alice",
        email="alice@example.com",
        first_name="Alice",
        last_name="Smith",
        phone="+1 555 0101",
    )
    u.set_password("supersecret1")
    _db.session.add(u)
    _db.session.commit()
    return u


@pytest.fixture()
def auth_client(client, user):
    """A test client already logged in as the ``user`` fixture."""
    client.post(
        "/auth/login",
        data={"identifier": "alice", "password": "supersecret1"},
        follow_redirects=True,
    )
    return client
