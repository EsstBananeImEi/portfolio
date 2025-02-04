# app/__init__.py
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Konfiguration laden (optional: app.config.from_object('config.Config'))

    # Blueprints oder Routen importieren und registrieren
    from app.routes import main  # Beispiel, wenn du Routen in routes.py hast

    app.register_blueprint(main)

    return app
