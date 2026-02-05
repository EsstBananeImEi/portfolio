from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
login_manager.login_view = "auth.login"  # type: ignore


@login_manager.user_loader
def load_user(user_id):
    """
    User-Loader für Flask-Login.
    Lädt Admin-User (id="1") oder Portfolio-Users (id="portfolio_<id>")
    """
    if user_id == "1":
        # Admin-User laden
        from app.auth.routes import VirtualAdminUser
        from flask import current_app

        admin_username = current_app.config.get("ADMIN_USERNAME", "admin")
        return VirtualAdminUser(admin_username)
    elif user_id.startswith("portfolio_"):
        # Portfolio-User laden
        from app.models import AccessRequest

        try:
            actual_id = int(user_id.replace("portfolio_", ""))
            user = AccessRequest.query.get(actual_id)

            # User zurückgeben wenn Account aktiv und genehmigt ist
            # Token-Ablauf wird NICHT hier geprüft, sondern in is_access_valid()
            # So kann sich der User auch mit abgelaufenem Token einloggen
            if user and user.is_active and user.status == "approved":
                return user
        except (ValueError, AttributeError):
            return None

    return None
