import pytest

from app import create_app
from app.extensions import db
from app.models import User
from app.security.passwords import hash_password


@pytest.fixture
def client():
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-secret-key",
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
    })

    with app.app_context():
        db.create_all()

        user = User(
            full_name="Emmy Test",
            email="emmy@example.com",
            password_hash=hash_password("CorrectPassword123!")
        )

        db.session.add(user)
        db.session.commit()

        user_id = user.id

    with app.test_client() as test_client:
        yield test_client

    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_successful_login(client):
    response = client.post("/login", data={
        "email": "emmy@example.com",
        "password": "CorrectPassword123!"
    })

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")


def test_login_with_wrong_password(client):
    response = client.post("/login", data={
        "email": "emmy@example.com",
        "password": "WrongPassword123!"
    }, follow_redirects=True)

    assert b"Invalid email or password." in response.data


def test_login_with_unknown_email(client):
    response = client.post("/login", data={
        "email": "unknown@example.com",
        "password": "CorrectPassword123!"
    }, follow_redirects=True)

    assert b"Invalid email or password." in response.data