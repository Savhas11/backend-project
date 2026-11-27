from flask import Flask, jsonify
from .main import main_bp
from .auth import auth_bp
from .extensions import db, migrate
from .config import config_options
from . import models

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_options[config_name])

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(400)
    def handle_bad_request(error):
        return jsonify({"error": "Bad request"}), 400

    @app.errorhandler(401)
    def handle_unauthorized(error):
        return jsonify({"error": "Unauthorized"}), 401

    @app.errorhandler(403)
    def handle_forbidden(error):
        return jsonify({"error": "Forbidden"}), 403

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(500)
    def handle_internal_error(error):
        return jsonify({"error": "Internal server error"}), 500

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app