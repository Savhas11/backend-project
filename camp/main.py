from flask import Blueprint, request, jsonify, g, current_app
import jwt

main_bp = Blueprint("main", __name__)


@main_bp.before_request
def authenticate_request():
    if request.endpoint in ["main.health", "auth.register", "auth.login"]:
        return None

    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Authorization header missing or invalid"}), 401

    token = auth_header.split(" ", 1)[1]

    try:
        payload = jwt.decode(
            token,
            current_app.config["JWT_SECRET_KEY"],
            algorithms=["HS256"]
        )

        g.user_id = int(payload["sub"])

    except (jwt.InvalidTokenError, KeyError, ValueError, TypeError):
        return jsonify({"error": "Invalid or expired token"}), 401


@main_bp.route("/health")
def health():
    return {"status": "ok"}, 200


@main_bp.route("/trails", methods=["GET"])
def get_trails():
    return jsonify([
        {
            "id": 1,
            "name": "Raven Run",
            "location": "Lexington, KY",
            "difficulty": "Moderate"
        },
        {
            "id": 2,
            "name": "Natural Bridge",
            "location": "Slade, KY",
            "difficulty": "Easy"
        }
    ])

    

