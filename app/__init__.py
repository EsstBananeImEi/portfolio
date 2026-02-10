from flask import Flask
import os
from .extensions import db, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config.get("DATABASE_URI")
    # SECRET_KEY wird bereits aus config.Config geladen, nicht überschreiben
    # Falls Sie eine Umgebungsvariable verwenden möchten, wird sie in config.py mit Fallback geladen
    print(app.config["SQLALCHEMY_DATABASE_URI"])  # Debug-Ausgabe der Datenbank-URI
    db.init_app(app)
    login_manager.init_app(app)

    # Session initialisieren (für Token-Verwaltung in DB)
    try:
        from flask_session import Session

        app.config["SESSION_SQLALCHEMY"] = db
        Session(app)
    except ImportError:
        pass  # flask-session nicht installiert

    # E-Mail initialisieren
    try:
        from app.email_utils import init_mail

        init_mail(app)
    except Exception:
        pass  # E-Mail nicht konfiguriert

    # Custom Jinja2 Filter für DevIcon SVG Pfade
    @app.template_filter("devicon_svg")
    def devicon_svg_filter(icon_class):
        """Konvertiert DevIcon-Klassen zu SVG-Pfaden"""
        import re

        match = re.search(r"devicon-(\w+)-(\w+)", icon_class)
        if match:
            name, variant = match.groups()
            return f"icons/skills/svg/{name}-{variant}.svg"
        return None

    from app.main.routes import main
    from app.auth.routes import auth
    from app.admin.routes import admin
    from app.auth.reset_password import reset

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(admin)
    app.register_blueprint(reset, url_prefix="/auth")

    return app
