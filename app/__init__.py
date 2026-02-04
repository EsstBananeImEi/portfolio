from flask import Flask
import os
from .extensions import db, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///portfolio.db"
    # SECRET_KEY wird bereits aus config.Config geladen, nicht überschreiben
    # Falls Sie eine Umgebungsvariable verwenden möchten, wird sie in config.py mit Fallback geladen

    db.init_app(app)
    login_manager.init_app(app)
    
    # Session initialisieren (für Token-Verwaltung in DB)
    from flask_session import Session
    app.config['SESSION_SQLALCHEMY'] = db
    Session(app)
    
    # E-Mail initialisieren
    from app.email_utils import init_mail
    init_mail(app)

    from app.main.routes import main
    from app.auth.routes import auth
    from app.admin.routes import admin

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(admin)

    return app
