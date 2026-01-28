from flask import Flask
# Import db and bcrypt from your database.py to initialize them
from app.database import db, bcrypt, init_db

def create_app(test_config=None):
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'uploads' # Required by your routes.py

    # Apply test config
    if test_config:
        app.config.update(test_config)

    # Initialize Plugins
    init_db(app)

    # Your routes.py defines 'main', so we import and register it here
    from app.routes import main
    app.register_blueprint(main)
    # ----------------------------
    
    return app