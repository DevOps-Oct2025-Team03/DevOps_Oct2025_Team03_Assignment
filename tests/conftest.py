import pytest
from flask import Flask
from app.config import Config
from app.database import db, init_db
 
@pytest.fixture()
def app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
 
    init_db(app)
 
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
 
@pytest.fixture()
def session(app):
    with app.app_context():
        yield db.session