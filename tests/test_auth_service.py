from app import create_app
from app.extensions import db
from app.models import User
from app.services.auth_service import register_user
from werkzeug.security import check_password_hash

def setup_test_database():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite://"
    })

    with app.app_context():
        db.create_all()

    return app

def test_successful_registration():
    app = setup_test_database()

    with app.app_context():
        user, error = register_user(
            "Emmy Test",
            "emmy.registration@example.com",
            "FinFlowTest123!"
        )

        assert user is not None
        assert error is None

        saved_user = User.query.filter_by(
            email="emmy.registration@example.com"
        ).first()

        assert saved_user is not None

        assert check_password_hash(
            saved_user.password_hash,
            "FinFlowTest123!"
        )