from flask import Blueprint

main_bp = Blueprint("hikes", __name__)


@main_bp.route("/health")
def health():
    return {"status": "ok"}, 200
