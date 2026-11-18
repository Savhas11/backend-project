from flask import Flask
from .main import main_bp
from .auth import auth_bp
from .extensions import db, migrate
from .config import config_options
from . import models


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_options[config_name])
    


    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app