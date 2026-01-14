#HTTP routes ( the endpoints )

from flask import Blueprint, jsonify
from .database import db
from uuid import uuid4


main = Blueprint("main", __name__)

@main.route("/", methods=["GET"])
def index():
    return jsonify(message="Flask app running")

@main.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok")

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