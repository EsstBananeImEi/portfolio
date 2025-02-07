from flask import Flask
from .extensions import db


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.Config")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///portfolio.db"

    db.init_app(app)

    # Blueprints oder Routen importieren und registrieren
    from app.routes import main  # Beispiel, wenn du Routen in routes.py hast

    app.register_blueprint(main)

    return app
