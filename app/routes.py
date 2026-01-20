#HTTP routes ( the endpoints )

from flask import Blueprint, jsonify, request, redirect, session, render_template, abort
from .database import db, bcrypt, User, File

from uuid import uuid4
from functools import wraps
import os

main = Blueprint("main", __name__)

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("role") != "admin":
            abort(403)
        return f(*args, **kwargs)
    return wrapper


@main.route("/", methods=["GET"])
def index():
    return jsonify(message="Flask app running")

@main.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok"), 200

@main.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@main.route("/admin", methods=["GET"])
@admin_required
def admin_dashboard():
    users = User.query.all()
    return render_template("admin.html", users=users)



@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        print("DEBUG login attempt:", username, password)

        user = User.query.filter_by(username=username).first()
        print("DEBUG user found:", user)

        if user and bcrypt.check_password_hash(user.password_hash, password):
            session.clear()
            session["user_id"] = user.id
            session["role"] = user.role

            print("DEBUG role:", user.role)

            if user.role == "admin":
                print("DEBUG redirecting to /admin")
                return redirect("/admin")

            print("DEBUG redirecting to /dashboard")
            return redirect("/dashboard")

        print("DEBUG invalid credentials")
        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")



@main.route("/admin/create_user", methods=["POST"])
@admin_required
def create_user():
    username = request.form.get("username")
    password = request.form.get("password")
    role = request.form.get("role", "user")

    if not username or not password:
        abort(400)

    if User.query.filter_by(username=username).first():
        return redirect("/admin")

    u = User(username=username, role=role)
    u.set_password(password)

    db.session.add(u)
    db.session.commit()
    return redirect("/admin")

@main.route("/admin/delete_user/<int:id>", methods=["POST"])
@admin_required
def delete_user(id):
    if id == session.get("user_id"):
        return redirect("/admin")  # prevent self-delete

    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/admin")

@main.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    if session.get("role") == "admin":
        return redirect("/admin")

    files = File.query.filter_by(owner_id=session["user_id"]).all()
    return render_template("dashboard.html", files=files)


# @main.route("/debug/create-user")
# def debug_create_user():
#     try:
#         username = f"demo_{uuid4().hex[:8]}"  # unique each time
#         u = User(username=username, role="user")
#         u.set_password("Password123!")
#         db.session.add(u)
#         db.session.commit()
#         return jsonify(username=u.username, password_hash=u.password_hash)
#     except Exception as e:
#         db.session.rollback()
#         return jsonify(error=str(e)), 500