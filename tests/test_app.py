import pytest
from app import create_app
from app.database import db, User

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Use fast in-memory DB
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client

def test_admin_access(client):
    """Test that only admins can reach the /admin route"""
    # 1. Test Unauthenticated
    res = client.get('/admin')
    assert res.status_code == 302 # Redirect to login

    # 2. Test as Regular User
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['role'] = 'user'
    res = client.get('/admin')
    assert res.status_code == 403 # Forbidden

