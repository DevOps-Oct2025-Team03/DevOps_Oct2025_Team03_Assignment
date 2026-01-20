import pytest
import io
from app.database import db, User, File

# =========================
# 1. ADMIN ACTIONS (Success & Fail)
# =========================

def test_admin_create_user_success(client):
    """SUCCESS: Admin creates a new user account."""
    # Simulate an active Admin session
    with client.session_transaction() as sess:
        sess['user_id'] = 99
        sess['role'] = 'admin'
    
    res = client.post('/admin/create_user', data={
        'username': 'staff_member',
        'password': 'password123',
        'role': 'user'
    }, follow_redirects=True)
    
    assert res.status_code == 200
    # Verify DB entry
    with client.application.app_context():
        user = User.query.filter_by(username='staff_member').first()
        assert user is not None
        assert user.role == 'user'

def test_admin_create_user_fail_missing_data(client):
    """FAIL: Admin attempts to create user without a password."""
    with client.session_transaction() as sess:
        sess['user_id'] = 99
        sess['role'] = 'admin'
    
    # Missing 'password' field triggers abort(400)
    res = client.post('/admin/create_user', data={'username': 'no_pass_user'})
    assert res.status_code == 400

def test_admin_delete_self_fail(client):
    """FAIL: Admin is blocked from deleting their own account."""
    with client.session_transaction() as sess:
        sess['user_id'] = 99
        sess['role'] = 'admin'
    
    # Logic prevents user_id == session.get("user_id")
    res = client.post('/admin/delete_user/99')
    assert res.status_code == 400

# =========================
# 2. USER FILE ACTIONS (Success & Fail)
# =========================

def test_user_file_operations_success(client):
    """SUCCESS: User can upload and then delete their own file."""
    with client.application.app_context():
        u = User(username="owner", role="user")
        # 🛠️ FIX: Set the password so password_hash is not NULL
        u.set_password("testpassword") 
        db.session.add(u)
        db.session.commit()
        u_id = u.id

    with client.session_transaction() as sess:
        sess['user_id'] = u_id
        sess['role'] = 'user'

    # Test Upload
    data = {'file': (io.BytesIO(b"file content"), 'my_report.txt')}
    client.post('/dashboard/upload', data=data, content_type='multipart/form-data')
    
    with client.application.app_context():
        f = File.query.filter_by(owner_id=u_id).first()
        assert f is not None
        file_id = f.id

    # Test Delete
    res_del = client.post(f'/dashboard/delete/{file_id}', follow_redirects=True)
    assert res_del.status_code == 200
    with client.application.app_context():
        assert File.query.get(file_id) is None

def test_user_data_isolation_fail(client):
    """FAIL: User B cannot download or delete User A's file."""
    with client.application.app_context():
        u_a = User(username="isolation_user_a", role="user")
        u_b = User(username="isolation_user_b", role="user")
        u_a.set_password("password_a")
        u_b.set_password("password_b")
        db.session.add_all([u_a, u_b])
        db.session.commit()

        # 🛠️ CAPTURE THE ID HERE while the session is active
        user_b_id = u_b.id 

        # User A uploads a file
        f = File(
            original_filename="secret.txt",
            stored_filename="unique_isolation_file_123.txt",
            size_bytes=10,
            owner_id=u_a.id
        )
        db.session.add(f)
        db.session.commit()
        file_id = f.id

    # 🛠️ Now user_b_id is just a number, so it won't crash outside the block
    with client.session_transaction() as sess:
        sess['user_id'] = user_b_id #
        sess['role'] = 'user'

    # Attempt unauthorized access
    res_down = client.get(f'/dashboard/download/{file_id}')
    res_del = client.post(f'/dashboard/delete/{file_id}')
    
    assert res_down.status_code == 404
    assert res_del.status_code == 404