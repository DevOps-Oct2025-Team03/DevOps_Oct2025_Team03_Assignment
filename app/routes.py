# from flask import Blueprint, jsonify, request, redirect, session, abort
# from functools import wraps

# from .database import db, bcrypt, User, File

# main = Blueprint("main", __name__)

# # =========================
# # Auth Decorators
# # =========================

# def login_required(f):
#     @wraps(f)
#     def wrapper(*args, **kwargs):
#         if "user_id" not in session:
#             return redirect("/login")
#         return f(*args, **kwargs)
#     return wrapper


# def admin_required(f):
#     @wraps(f)
#     def wrapper(*args, **kwargs):
#         if "user_id" not in session:
#             return redirect("/login")
#         if session.get("role") != "admin":
#             abort(403)
#         return f(*args, **kwargs)
#     return wrapper


# # =========================
# # Health / Index
# # =========================

# @main.route("/", methods=["GET"])
# def index():
#     return jsonify(message="Flask app running"), 200


# @main.route("/health", methods=["GET"])
# def health():
#     return jsonify(status="ok"), 200


# # =========================
# # Login / Logout
# # =========================

# @main.route("/login", methods=["POST"])
# def login():
#     username = request.form.get("username")
#     password = request.form.get("password")

#     if not username or not password:
#         return "Invalid credentials", 401

#     user = User.query.filter_by(username=username).first()

#     if not user or not bcrypt.check_password_hash(user.password_hash, password):
#         return "Invalid credentials", 401

#     session.clear()
#     session["user_id"] = user.id
#     session["role"] = user.role

#     if user.role == "admin":
#         return redirect("/admin")

#     return redirect("/dashboard")


# @main.route("/logout", methods=["GET"])
# def logout():
#     session.clear()
#     return redirect("/login")


# # =========================
# # User Dashboard
# # =========================

# @main.route("/dashboard", methods=["GET"])
# @login_required
# def dashboard():
#     if session.get("role") == "admin":
#         return redirect("/admin")

#     files = File.query.filter_by(owner_id=session["user_id"]).all()

#     return jsonify(
#         files=[
#             {
#                 "id": f.id,
#                 "filename": f.original_filename,
#                 "size": f.size_bytes,
#             }
#             for f in files
#         ]
#     ), 200


# # =========================
# # Admin Dashboard
# # =========================

# @main.route("/admin", methods=["GET"])
# @admin_required
# def admin_dashboard():
#     users = User.query.all()

#     return jsonify(
#         users=[
#             {
#                 "id": u.id,
#                 "username": u.username,
#                 "role": u.role,
#             }
#             for u in users
#         ]
#     ), 200


# # =========================
# # Admin: Create User
# # =========================

# @main.route("/admin/create_user", methods=["POST"])
# @admin_required
# def create_user():
#     username = request.form.get("username")
#     password = request.form.get("password")
#     role = request.form.get("role", "user")

#     if not username or not password:
#         abort(400)

#     if role not in ("user", "admin"):
#         abort(400)

#     if User.query.filter_by(username=username).first():
#         abort(409)

#     u = User(username=username, role=role)
#     u.set_password(password)

#     db.session.add(u)
#     db.session.commit()

#     return jsonify(message="User created"), 201


# # =========================
# # Admin: Delete User
# # =========================

# @main.route("/admin/delete_user/<int:user_id>", methods=["POST"])
# @admin_required
# def delete_user(user_id):
#     if user_id == session.get("user_id"):
#         abort(400)  # prevent self-delete

#     user = User.query.get_or_404(user_id)

#     db.session.delete(user)
#     db.session.commit()

#     return jsonify(message="User deleted"), 200





from flask import Blueprint, jsonify, request, redirect, session, abort, render_template
from functools import wraps
from .database import db, bcrypt, User, File

main = Blueprint("main", __name__)


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
    # Requirement says GET/POST.
    # We keep it backend-safe (no templates).
    if request.method == "GET":
        return (
            jsonify(
                message="Login endpoint. POST username/password to authenticate.",
                fields=["username", "password"],
            ),
            200,
        )

    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return "Invalid credentials", 401

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return "Invalid credentials", 401

    session.clear()
    session["user_id"] = user.id
    session["role"] = user.role

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
    if session.get("role") == "admin":
        return redirect("/admin")

    files = File.query.filter_by(owner_id=session["user_id"]).all()
    return jsonify(
        files=[
            {"id": f.id, "filename": f.original_filename, "size": f.size_bytes}
            for f in files
        ]
    ), 200


# =========================
# Admin Dashboard
# =========================
@main.route("/admin", methods=["GET"])
@admin_required
def admin_dashboard():
    users = User.query.all()
    return render_template("admin.html", users=users)


# =========================
# Admin: Create User
# =========================
@main.route("/admin/create_user", methods=["POST"])
@admin_required
def create_user():
    username = request.form.get("username")
    password = request.form.get("password")
    role = request.form.get("role", "user")

    if not username or not password:
        abort(400)

    if role not in ("user", "admin"):
        abort(400)

    if User.query.filter_by(username=username).first():
        abort(409)

    u = User(username=username, role=role)
    u.set_password(password)

    db.session.add(u)
    db.session.commit()

    return jsonify(message="User created"), 201


# =========================
# Admin: Delete User
# =========================
@main.route("/admin/delete_user/<int:user_id>", methods=["POST"])
@admin_required
def delete_user(user_id):
    if user_id == session.get("user_id"):
        abort(400)  # prevent self-delete

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return jsonify(message="User deleted"), 200
