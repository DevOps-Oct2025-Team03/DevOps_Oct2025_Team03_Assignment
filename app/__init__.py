from flask import Flask
from .database import db, bcrypt
from .config import Config # Import your config file
 
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config) # This tells Flask WHERE the database is
 
    db.init_app(app)
    bcrypt.init_app(app)
    # Register your routes/blueprints here
    from .routes import main
    app.register_blueprint(main)
 
    return app