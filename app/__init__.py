
import os

from flask import Flask, app
from app.extensions import db


def create_app(test_config=None):
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get(
        "FINFLOW_SECRET_KEY",
        "local-development-only-change-before-deployment"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///finflow.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from app.models import User

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app