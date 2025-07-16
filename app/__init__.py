# __init__.py

from flask import Flask
from .config import Config
from .models import db
from .routes import bp as main_bp
from typing import Any  # можно не импортировать, если не используется


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(main_bp)
    return app
