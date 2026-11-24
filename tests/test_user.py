from app import create_app
from app.extensions import db
from app.models import User
from sqlalchemy import inspect
from werkzeug.security import generate_password_hash, check_password_hash

def setup_test_database():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite://"
    })

    with app.app_context():
        db.create_all()

    return app


def test_user_table_name():
    assert User.__tablename__ == "users"

def test_database_setup():
    app = setup_test_database()

    with app.app_context():
        table_names = inspect(db.engine).get_table_names()


        assert "users" in table_names

def test_create_user():
    app = setup_test_database()

    with app.app_context():
        user = User(
            full_name="Emmy Test",
            email="emmy.test@example.com",
            password_hash=generate_password_hash("FinFlowTest123!")
        )

        db.session.add(user)
        db.session.commit()

        saved_user = db.session.get(User, user.id)

        assert saved_user is not None