
import os
from flask import Flask
from .database import db, bcrypt
from .config import Config
from .seed import seed

def create_app(test_config=None):
    """
    Application Factory Pattern.
    This allows the app to be created with different configs for 
    Production, Development, and Testing (Pytest/Behave).
    """
    app = Flask(__name__)

    # 1. Load Configuration
    if test_config is None:
        # Load from the Config class in config.py
        app.config.from_object(Config)
    else:
        # Load the testing config (e.g., from conftest.py or environment.py)
        app.config.update(test_config)

    # 2. Initialization of Plugins
    db.init_app(app)
    bcrypt.init_app(app)

    # 3. Security: Ensure the Uploads folder exists
    # This prevents errors during the File Management tests
    upload_path = app.config.get('UPLOAD_FOLDER', 'uploads')
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)

    # 4. Register Blueprints
    # Importing here prevents "Circular Import" errors
    from .routes import main
    app.register_blueprint(main)

    # 5. Database Setup
    with app.app_context():
        # Creates SQLite/Postgres tables based on models
        db.create_all()
        
        # Seed the database only if we are NOT testing
        # This keeps your Behave tests clean and predictable
        if not app.config.get("TESTING"):
            seed()

    return app