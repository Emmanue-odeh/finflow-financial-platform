from app.extensions import db
from app.models import User
from app.security.passwords import hash_password, verify_password

def register_user(full_name, email, password):
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return None, "An account with this email already exists."
    password_hash = hash_password(password)

    new_user = User(
        full_name=full_name,
        email=email,
        password_hash=password_hash
    )

    db.session.add(new_user)
    db.session.commit()
    return new_user, None


def login_user(email, password):
    user = User.query.filter_by(email=email).first()

    if not user:
        return None, "Invalid email or password."

    if not verify_password(user.password_hash, password):
        return None, "Invalid email or password."

    if not user.is_active:
        return None, "This account is currently inactive."

    return user, None