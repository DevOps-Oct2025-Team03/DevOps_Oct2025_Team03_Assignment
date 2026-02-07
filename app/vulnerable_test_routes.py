"""
INTENTIONALLY VULNERABLE CODE FOR SAST TESTING
Purpose: Validate that CodeQL detects security issues
DO NOT deploy to production.
"""
import os
import hashlib
import subprocess
from flask import Blueprint, request, jsonify, send_file, make_response
from .database import db

vuln_test = Blueprint('vuln_test', __name__)


# SAST-01: SQL Injection (CWE-89) — query is EXECUTED
@vuln_test.route("/test/search", methods=["GET"])
def search_user():
    username = request.args.get("username")
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    result = db.session.execute(db.text(query))
    return jsonify([dict(row) for row in result])


# SAST-02: Hardcoded Credentials (CWE-798) — used in a route
@vuln_test.route("/test/db-check", methods=["GET"])
def db_check():
    import psycopg2
    conn = psycopg2.connect(
        host="localhost",
        database="myapp",
        user="admin",
        password="SuperSecret123!"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    conn.close()
    return jsonify({"status": "connected"})


# SAST-03: Path Traversal (CWE-22)
@vuln_test.route("/test/download", methods=["GET"])
def download_file():
    filename = request.args.get("file")
    filepath = os.path.join("/app/uploads", filename)
    return send_file(filepath)


# SAST-04: Weak Password Hashing (CWE-327) — used in a route
@vuln_test.route("/test/hash", methods=["GET"])
def hash_test():
    password = request.args.get("password")
    hashed = hashlib.md5(password.encode()).hexdigest()
    return jsonify({"hash": hashed})


# SAST-05: Flask Debug Mode (CWE-215)
def run_debug_server(app):
    app.run(host="0.0.0.0", port=5000, debug=True)


# SAST-06: Reflected XSS (CWE-79) — adding this for stronger detection
@vuln_test.route("/test/greet", methods=["GET"])
def greet():
    name = request.args.get("name", "Guest")
    html = "<html><body><h1>Hello, " + name + "!</h1></body></html>"
    return make_response(html)


# SAST-07: OS Command Injection (CWE-78) — adding this for stronger detection
@vuln_test.route("/test/ping", methods=["GET"])
def ping_host():
    hostname = request.args.get("host")
    output = subprocess.check_output("ping -c 1 " + hostname, shell=True)
    return output.decode()