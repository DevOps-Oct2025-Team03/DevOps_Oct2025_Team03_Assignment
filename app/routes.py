from flask import Blueprint, jsonify, request, redirect, session, abort, render_template
from functools import wraps
from .database import db, bcrypt, User, File
import os
from flask import send_from_directory, flash
from werkzeug.utils import secure_filename
import uuid
import re

main = Blueprint("main", __name__)

# Helper function

def is_password_strong(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Za-z]", password): # at least 1 letter 
        return False
    if not re.search(r"\d", password): # at least 1 number
        return False
    return True



# =========================
# Auth Decorators
# =========================
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
        if "user_id" not in session:
            return redirect("/login")
        if session.get("role") != "admin":
            abort(403)
        return f(*args, **kwargs)
    return wrapper


# =========================
# Health / Index
# =========================
@main.route("/", methods=["GET"])
def index():
    return jsonify(message="Flask app running"), 200


@main.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok"), 200


# =========================
# Login / Logout
# =========================
@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return "Invalid credentials", 401

    session.clear()
    session["user_id"] = user.id
    session["role"] = user.role

    # RBAC Redirection: Admin goes to /admin, User goes to /dashboard
    if user.role == "admin":
        return redirect("/admin")
    return redirect("/dashboard")

@main.route("/logout", methods=["GET"])
def logout():
    session.clear() 
    return redirect("/login")

# =========================
# User Dashboard
# =========================
@main.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    # If an admin accidentally visits /dashboard, send them to /admin
    if session.get("role") == "admin":
        return redirect("/admin")

    # DATA ISOLATION: Each user can ONLY see their own files
    user_files = File.query.filter_by(owner_id=session["user_id"]).all()
    return render_template("dashboard.html", files=user_files)

# =========================
# File Management (Authenticated Users)
# =========================
import uuid  # Add this at the top of routes.py

@main.route("/dashboard/upload", methods=["POST"])
@login_required
def upload_file():
    if 'file' not in request.files:
        return redirect("/dashboard")
    
    file = request.files['file']
    if file.filename == '':
        return redirect("/dashboard")

    if file:
        original_name = secure_filename(file.filename)
        
        # Create a unique name for the storage folder
        unique_id = str(uuid.uuid4())
        extension = os.path.splitext(original_name)[1]
        stored_name = f"{unique_id}{extension}"

        # Ensure the directory exists
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # SAVE the actual file bytes to the disk
        file.save(os.path.join(UPLOAD_FOLDER, stored_name))

        # Save record to Database
        new_file = File(
            original_filename=original_name,
            stored_filename=stored_name,
            size_bytes=0, # Optional: os.path.getsize(path)
            owner_id=session["user_id"]
        )
        db.session.add(new_file)
        db.session.commit()
        
    return redirect("/dashboard")

# In routes.py
@main.route("/dashboard/download/<int:file_id>", methods=["GET"])
@login_required
def download_file(file_id):
    # This triggers a 404 if the file_id doesn't belong to the logged-in user
    f = File.query.filter_by(id=file_id, owner_id=session["user_id"]).first_or_404()
    
    return send_from_directory(
        directory=os.path.abspath(UPLOAD_FOLDER), 
        path=f.stored_filename, 
        download_name=f.original_filename,
        as_attachment=True
    )

@main.route("/dashboard/delete/<int:file_id>", methods=["POST"])
@login_required
def delete_file(file_id):
    # Security: Ensure the user cannot delete someone else's file
    f = File.query.filter_by(id=file_id, owner_id=session["user_id"]).first_or_404()
    db.session.delete(f)
    db.session.commit()
    return redirect("/dashboard")


# =========================
# Admin Dashboard
# =========================
@main.route("/admin", methods=["GET"])
@admin_required
def admin_dashboard():
    # Displays a list of all registered user accounts
    users = User.query.all()
    return render_template("admin.html", users=users)


@main.route("/admin/create_user", methods=["POST"])
@admin_required
def create_user():
    username = request.form.get("username")
    password = request.form.get("password")
    role = request.form.get("role", "user")

    if not username or not password:
        abort(400)

    if not is_password_strong(password):
        return "Password does not meet complexity requirements", 400

    if role not in ("user", "admin"):
        abort(400)

    if User.query.filter_by(username=username).first():
        abort(409)

    u = User(username=username, role=role)
    u.set_password(password)

    db.session.add(u)
    db.session.commit()

    return redirect("/admin")



@main.route("/admin/delete_user/<int:user_id>", methods=["POST"])
@admin_required
def delete_user(user_id):
    # Security check: Prevent deleting yourself
    if user_id == session.get("user_id"):
        abort(400)

    user = User.query.get_or_404(user_id)
    db.session.delete(user) # Admin can remove user accounts
    db.session.commit()

    # Success: Redirect back to Admin dashboard
    return redirect("/admin")


# Configuration - Ensure this folder exists in your Docker container
UPLOAD_FOLDER = 'uploads'



