# import sys
# import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# import pytest
# from flask import Flask
# from app.config import Config
# from app.database import db, init_db, User
# from app.routes import main


# @pytest.fixture()
# def app():
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     app.config["TESTING"] = True
#     app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
#     app.config["SESSION_COOKIE_SECURE"] = False
#     app.secret_key = "test-secret"

#     init_db(app)
#     app.register_blueprint(main)

#     with app.app_context():
#         db.create_all()

#         admin = User(username="admin_user", role="admin")
#         admin.set_password("admin123")

#         user = User(username="user_a", role="user")
#         user.set_password("user123")

#         db.session.add_all([admin, user])
#         db.session.commit()

#         yield app

#         db.session.remove()
#         db.drop_all()


# @pytest.fixture()
# def client(app):
#     return app.test_client()


# @pytest.fixture()
# def session(app):
#     with app.app_context():
#         yield db.session




import pytest
from app import create_app
from app.database import db, User


@pytest.fixture()
def app():
    app = create_app()

    # override config for tests
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SESSION_COOKIE_SECURE"] = False

    with app.app_context():
        db.drop_all()
        db.create_all()

        admin = User(username="admin_user", role="admin")
        admin.set_password("admin123")

        user = User(username="user_a", role="user")
        user.set_password("user123")

        db.session.add_all([admin, user])
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def session(app):
    with app.app_context():
        yield db.session




