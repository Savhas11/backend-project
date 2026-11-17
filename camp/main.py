from flask import Blueprint
from flask import request, jsonify
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone
from .extensions import db
from .models import User

main_bp = Blueprint("hikes", __name__)


@main_bp.route("/health")
def health():
    return {"status": "ok"}, 200


@main_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    if not isinstance(email, str) or not 5 <= len(email) <= 220:
        return jsonify({"error": "Email must be between 5 and 220 characters"}), 400

    if not isinstance(password, str) or not 8 <= len(password) <= 128:
        return jsonify({"error": "Password must be between 8 and 128 characters"}), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"error": "Email already registered"}), 409

    password_hash = generate_password_hash(password)

    new_user = User(
        email=email,
        password_hash=password_hash,
        created_at=datetime.now(timezone.utc)
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "id": new_user.id,
        "email": new_user.email,
        "created_at": new_user.created_at.isoformat()
    }), 201