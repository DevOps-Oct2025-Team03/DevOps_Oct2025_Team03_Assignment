import pytest
from app.database import db, User

def test_password_is_hashed(app):
    """
    Verifies that the database stores hashed passwords.
    Fixes IntegrityError by providing a mandatory 'role'.
    """
    with app.app_context():
        raw_password = "SecretPassword123"
        # Explicitly set the role to satisfy the NOT NULL constraint
        user = User(username="test_secure_user", role="user") 
        user.set_password(raw_password)
        db.session.add(user)
        db.session.commit()

        db_user = User.query.filter_by(username="test_secure_user").first()
        
        assert db_user.password_hash != raw_password, "FAIL: Plain text stored!"
        assert db_user.password_hash.startswith('$2b$'), "FAIL: Invalid hash format!"