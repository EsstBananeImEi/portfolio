from flask import Flask
import os
from .extensions import db, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///portfolio.db"
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    db.init_app(app)
    login_manager.init_app(app)

    from app.main.routes import main
    from app.auth.routes import auth
    from app.admin.routes import admin

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(admin)

    return app
