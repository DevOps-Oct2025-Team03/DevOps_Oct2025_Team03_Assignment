import os
import shutil
from app import create_app
from app.database import db

# Define upload folder for testing
UPLOAD_FOLDER = 'uploads'

def before_all(context):
    # Ensure environment is set to testing
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    # Create app with test config
    context.app = create_app(test_config={
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'UPLOAD_FOLDER': UPLOAD_FOLDER
    })
    
    # Push Context
    context.app_context = context.app.app_context()
    context.app_context.push()
    
    # Initialize DB
    db.create_all()
    
    # Create Test Client
    context.client = context.app.test_client()
    
    # Create Upload Folder
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

def after_all(context):
    db.session.remove()
    db.drop_all()
    context.app_context.pop()
    
    # Clean up files created during tests
    if os.path.exists(UPLOAD_FOLDER):
        shutil.rmtree(UPLOAD_FOLDER)

def after_scenario(context, scenario):
    db.session.rollback()
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()