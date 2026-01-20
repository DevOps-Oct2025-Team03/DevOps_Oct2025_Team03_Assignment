from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
import sqlite3
 
db = SQLAlchemy()
bcrypt = Bcrypt()
 
def init_db(app):
    db.init_app(app)
    bcrypt.init_app(app)
 
class User(db.Model):
    __tablename__ = "users"
 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
 
    files = db.relationship("File", backref="owner", cascade="all, delete-orphan")
 
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
 
class File(db.Model):
    __tablename__ = "files"
 
    id = db.Column(db.Integer, primary_key=True)
 
    # 🔐 DATA ISOLATION (THIS LINE IS CRITICAL)
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
 
    original_filename = db.Column(db.String(255), nullable=False)
    stored_filename = db.Column(db.String(255), unique=True, nullable=False)
    size_bytes = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)