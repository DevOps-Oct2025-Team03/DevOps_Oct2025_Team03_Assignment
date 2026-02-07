"""
INTENTIONALLY VULNERABLE CODE FOR SAST TESTING
Purpose: Validate that CodeQL detects security issues
DO NOT deploy to production.
"""
import os
import hashlib
from flask import Blueprint, request, jsonify, send_file

vuln_test = Blueprint('vuln_test', __name__)


# SAST-01: SQL Injection (CWE-89)
@vuln_test.route("/test/search", methods=["GET"])
def search_user():
    username = request.args.get("username")
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    return jsonify({"query": query})


# SAST-02: Hardcoded Credentials (CWE-798)
def get_db_connection():
    import psycopg2
    conn = psycopg2.connect(
        host="localhost",
        database="myapp",
        user="admin",
        password="SuperSecret123!"
    )
    return conn


# SAST-03: Path Traversal (CWE-22)
@vuln_test.route("/test/download", methods=["GET"])
def download_file():
    filename = request.args.get("file")
    filepath = os.path.join("/app/uploads", filename)
    return send_file(filepath)


# SAST-04: Weak Password Hashing (CWE-327)
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


# SAST-05: Flask Debug Mode (CWE-215)
def run_debug_server(app):
    app.run(host="0.0.0.0", port=5000, debug=True)