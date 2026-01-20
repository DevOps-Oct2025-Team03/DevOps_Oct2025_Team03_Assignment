from flask import Flask
from .database import db, bcrypt
from .config import Config
from .routes import main
from .seed import seed

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(main)

    with app.app_context():
        db.create_all()
        if not app.config.get("TESTING", False):
            seed()

    return 


