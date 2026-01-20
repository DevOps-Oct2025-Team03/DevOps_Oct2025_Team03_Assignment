import pytest


def test_login_success_redirects_to_dashboard(client):
    resp = client.post(
        "/login",
        data={
            "username": "user_a",
            "password": "user123",
        },
        follow_redirects=False,
    )

    assert resp.status_code in (302, 303)
    assert "/dashboard" in resp.headers["Location"]


def test_login_invalid_credentials_returns_401(client):
    resp = client.post(
        "/login",
        data={
            "username": "user_a",
            "password": "wrong",
        },
    )

    assert resp.status_code == 401
    assert b"Invalid credentials" in resp.data


def test_logout_redirects_to_login(client):
    client.post(
        "/login",
        data={
            "username": "user_a",
            "password": "user123",
        },
    )

    resp = client.get("/logout", follow_redirects=False)

    assert resp.status_code in (302, 303)
    assert "/login" in resp.headers["Location"]


def test_dashboard_requires_login(client):
    resp = client.get("/dashboard", follow_redirects=False)

    assert resp.status_code in (302, 303)
    assert "/login" in resp.headers["Location"]


def test_admin_blocked_for_regular_user(client):
    client.post(
        "/login",
        data={
            "username": "user_a",
            "password": "user123",
        },
    )

    resp = client.get("/admin")

    assert resp.status_code == 403


def test_admin_accessible_for_admin(client):
    client.post(
        "/login",
        data={
            "username": "admin_user",
            "password": "admin123",
        },
    )

    resp = client.get("/admin")

    assert resp.status_code == 200
    assert b"admin_user" in resp.data
