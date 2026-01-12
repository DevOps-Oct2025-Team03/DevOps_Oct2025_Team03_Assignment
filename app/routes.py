#HTTP routes ( the endpoints )

from flask import Blueprint, jsonify

main = Blueprint("main", __name__)

@main.route("/", methods=["GET"])
def index():
    return jsonify(message="Flask app running")

@main.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok")
