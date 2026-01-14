from flask import Flask
from .database import db, bcrypt
from .config import Config # Import your config file
 
def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        # This is the line that actually builds the tables in the DB container
        db.create_all()

    return app