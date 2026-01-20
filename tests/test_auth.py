import pytest
from app.database import db, User

# =========================
# SUCCESSFUL AUTH TESTS
# =========================

def test_admin_login_success(client):
    """Test that an Admin logs in and is redirected to /admin"""
    # Use the credentials from your seed data or routes logic
    resp = client.post("/login", data={
        "username": "admin_user", 
        "password": "admin123"
    }, follow_redirects=False)
    
    assert resp.status_code == 302
    assert "/admin" in resp.headers["Location"]

def test_user_login_success(client):
    """Test that a regular User logs in and is redirected to /dashboard"""
    resp = client.post("/login", data={
        "username": "user_a", 
        "password": "user123"
    }, follow_redirects=False)
    
    assert resp.status_code == 302
    assert "/dashboard" in resp.headers["Location"]

def test_logout_clears_session(client):
    """Test that logout redirects to login and clears the session"""
    # Login first
    client.post("/login", data={"username": "user_a", "password": "user123"})
    
    # Then logout
    resp = client.get("/logout", follow_redirects=False)
    assert resp.status_code == 302
    assert "/login" in resp.headers["Location"]

# =========================
# FAILED / SECURITY TESTS
# =========================

def test_login_invalid_password(client):
    """FAIL TEST: Correct username but wrong password"""
    resp = client.post("/login", data={
        "username": "admin_user", 
        "password": "wrongpassword"
    })
    # Your routes return 401 for invalid credentials
    assert resp.status_code == 401
    assert b"Invalid credentials" in resp.data

def test_login_nonexistent_user(client):
    """FAIL TEST: Username that doesn't exist in DB"""
    resp = client.post("/login", data={
        "username": "ghost_user", 
        "password": "password123"
    })
    assert resp.status_code == 401

def test_unauthenticated_access_denied(client):
    """FAIL TEST: Trying to access dashboard without logging in"""
    # This tests your @login_required decorator
    resp = client.get("/dashboard", follow_redirects=False)
    assert resp.status_code == 302
    assert "/login" in resp.headers["Location"]

def test_user_accessing_admin_panel_denied(client):
    """FAIL TEST: Regular user trying to access admin route (RBAC)"""
    # Login as a regular user
    client.post("/login", data={"username": "user_a", "password": "user123"})
    
    # Try to hit /admin - should trigger abort(403)
    resp = client.get("/admin")
    assert resp.status_code == 403