"""
REMEDIATED CODE — All SAST vulnerabilities fixed
"""
import os
from flask import Blueprint, request, jsonify, send_file, make_response
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from markupsafe import escape
from .database import db

vuln_test = Blueprint('vuln_test', __name__)


# SAST-01 FIXED: Parameterized query
@vuln_test.route("/test/search", methods=["GET"])
def search_user():
    username = request.args.get("username")
    result = db.session.execute(
        db.text("SELECT * FROM users WHERE username = :uname"),
        {"uname": username}
    )
    return jsonify([dict(row) for row in result])


# SAST-02 FIXED: Environment variables
@vuln_test.route("/test/db-check", methods=["GET"])
def db_check():
    import psycopg2
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD")
    )
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    conn.close()
    return jsonify({"status": "connected"})


# SAST-03 FIXED: Sanitized filename + path validation
@vuln_test.route("/test/download", methods=["GET"])
def download_file():
    filename = request.args.get("file")
    safe_name = secure_filename(filename)
    upload_dir = os.path.realpath("/app/uploads")
    filepath = os.path.realpath(os.path.join(upload_dir, safe_name))
    if not filepath.startswith(upload_dir):
        return jsonify({"error": "Access denied"}), 403
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404
    return send_file(filepath)


# SAST-04 FIXED: Strong hashing
@vuln_test.route("/test/hash", methods=["GET"])
def hash_test():
    password = request.args.get("password")
    hashed = generate_password_hash(password)
    return jsonify({"hash": hashed})


# SAST-05 FIXED: Debug + host from environment
def run_production_server(app):
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    app.run(host=host, port=5000, debug=debug_mode)


# SAST-06 FIXED: Escaped user input
@vuln_test.route("/test/greet", methods=["GET"])
def greet():
    name = request.args.get("name", "Guest")
    safe_name = escape(name)
    html = f"<html><body><h1>Hello, {safe_name}!</h1></body></html>"
    return make_response(html)


# SAST-07 FIXED: No shell, input validated
@vuln_test.route("/test/ping", methods=["GET"])
def ping_host():
    import subprocess
    hostname = request.args.get("host")
    if not hostname or not hostname.replace(".", "").isalnum():
        return jsonify({"error": "Invalid hostname"}), 400
    output = subprocess.check_output(["ping", "-c", "1", hostname])
    return output.decode()