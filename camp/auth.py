from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone, timedelta
from camp.extensions import db
from camp.models import User
import jwt

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if user is None or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    payload = {
        "sub": str(user.id),
        "role": "user",
        "exp": datetime.now(timezone.utc) + timedelta(
            seconds=current_app.config["JWT_LIFETIME_SECONDS"]
        )
    }

    print("JWT expiration:", payload["exp"])

    secret = current_app.config["JWT_SECRET_KEY"]
    algorithm = "HS256"
    token = jwt.encode(payload, secret, algorithm=algorithm)

    return jsonify({"token": token}), 200

@auth_bp.route("/register", methods=["POST"])
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