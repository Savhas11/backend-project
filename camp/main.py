from flask import Blueprint, request, jsonify, g, current_app
from .models import User
import jwt
from camp.models import User, Trail
from camp.extensions import db

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

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401

    except (jwt.InvalidTokenError, KeyError, ValueError, TypeError):
        return jsonify({"error": "Invalid token"}), 401


@main_bp.route("/health")
def health():
    return {"status": "ok"}, 200



@main_bp.route("/profile", methods=["GET"])
def get_profile():
    user = User.query.get(g.user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at.isoformat()
    }), 200



@main_bp.route("/profile", methods=["PATCH"])
def patch_profile():
    user = User.query.get(g.user_id)

    data = request.get_json() or {}

    if "email" in data:
        user.email = data["email"]

    db.session.commit()

    return jsonify({
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at.isoformat()
    }), 200

@main_bp.route("/admin/trails_test", methods=["GET"])
def trails_test():
    user = User.query.get(g.user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    if user.role != "admin":
        return jsonify({"error": "Admin access required"}), 403

    return jsonify({"message": "Admin only area"}), 200

    
    
@main_bp.route("/trails", methods=["POST"])
def create_trail():

    
    data = request.get_json()

    if "name" not in data or "distance_miles" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    if (
    not isinstance(data["distance_miles"], (int, float))
    or isinstance(data["distance_miles"], bool)
    or data["distance_miles"] <= 0
):
        return jsonify({"error": "distance_miles must be a positive number"}), 400

   
    trail = Trail(
        name=data["name"],
        distance_miles=data["distance_miles"],
        difficulty=data.get("difficulty"),
        description=data.get("description"),
        user_id=g.user_id
    )

    db.session.add(trail)
    db.session.commit()

 
    return jsonify({
        "id": trail.id,
        "name": trail.name,
        "distance_miles": trail.distance_miles,
        "difficulty": trail.difficulty,
        "description": trail.description,
        "user_id": trail.user_id
    }), 201

@main_bp.route("/trails", methods=["GET"])
def get_trails():

    trails = Trail.query.filter(Trail.user_id == g.user_id).all()

  
    trail_list = [
        {
            "id": trail.id,
            "name": trail.name,
            "distance_miles": trail.distance_miles,
            "difficulty": trail.difficulty,
            "description": trail.description
        }
        for trail in trails
    ]

    return jsonify(trail_list), 200

@main_bp.route("/trails/<int:trail_id>", methods=["GET"])
def get_trails_by_id(trail_id):

    trail = Trail.query.filter(
        Trail.id == trail_id,
        Trail.user_id == g.user_id
    ).first()

    if trail is None:
        return jsonify({"error": "trail not found"}), 404

    return jsonify({
        "id": trail.id,
        "name": trail.name,
        "distance_miles": trail.distance_miles,
        "difficulty": trail.difficulty,
        "description": trail.description
    }), 200

def get_owned_trail(trail_id):
    return Trail.query.filter(
        Trail.id == trail_id,
        Trail.user_id == g.user_id
    ).first()

@main_bp.route("/trails/<int:trail_id>", methods=["PATCH"])
def update_trail_by_id(trail_id):
    trail = get_owned_trail(trail_id)

    
    if trail is None:
        return jsonify({"error": "trail not found"}), 404

  
    data = request.get_json()

    if "distance_miles" in data:
        if (
            not isinstance(data["distance_miles"], (int, float))
            or isinstance(data["distance_miles"], bool)
            or data["distance_miles"] <= 0
        ):
            return jsonify({"error": "invalid distance_miles"}), 400

    
    if "name" in data:
        trail.name = data["name"]

    if "distance_miles" in data:
        trail.distance_miles = data["distance_miles"]

    if "difficulty" in data:
        trail.difficulty = data["difficulty"]

    if "description" in data:
        trail.description = data["description"]


    db.session.commit()

    return jsonify({
        "id": trail.id,
        "name": trail.name,
        "distance_miles": trail.distance_miles,
        "difficulty": trail.difficulty,
        "description": trail.description
    }), 200


@main_bp.route("/trails/<int:trail_id>", methods=["DELETE"])
def delete_trail_by_id(trail_id):

    trail = get_owned_trail(trail_id)

    
    if trail is None:
        return jsonify({"error": "trail not found"}), 404
    
    db.session.delete(trail)
    db.session.commit()

    return "", 204

