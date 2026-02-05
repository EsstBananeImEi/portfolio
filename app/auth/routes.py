from datetime import datetime
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    current_app,
)
from flask_login import login_user, logout_user, login_required
from app.models import Contact, AccessRequest
from werkzeug.security import check_password_hash


# Virtueller Admin-User (kein DB-Zugriff nötig)
class VirtualAdminUser:
    def __init__(self, username):
        self.id = 1
        self.username = username
        self.image = "default.png"
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return str(self.id)


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Admin-Login über Umgebungsvariable
        admin_username = current_app.config.get("ADMIN_USERNAME", "admin")
        admin_password_hash = current_app.config.get("ADMIN_PASSWORD_HASH")

        if not admin_password_hash:
            flash(
                "Admin-Passwort nicht konfiguriert. Bitte ADMIN_PASSWORD_HASH setzen.",
                "error",
            )
            return render_template(
                "auth/login.html", contact=Contact.query.first(), now=datetime.now()
            )

        if username == admin_username and check_password_hash(
            admin_password_hash, password
        ):
            # Erstelle virtuellen Admin-User für Session
            user = VirtualAdminUser(username)
            login_user(user)
            flash("Login erfolgreich!", "success")
            return redirect(url_for("main.index"))
        else:
            flash("Login fehlgeschlagen. Benutzername oder Passwort falsch.", "error")

    return render_template(
        "auth/login.html", contact=Contact.query.first(), now=datetime.now()
    )


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@auth.route("/portfolio-login", methods=["GET", "POST"])
def portfolio_login():
    """Login für genehmigte Portfolio-Benutzer"""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Bitte geben Sie E-Mail und Passwort ein.", "error")
            return render_template(
                "auth/portfolio_login.html",
                contact=Contact.query.first(),
                now=datetime.now(),
            )

        # Benutzer in AccessRequest-Tabelle suchen
        user = AccessRequest.query.filter_by(email=email).first()

        if user and user.password_hash and user.is_active and user.status == "approved":
            # Passwort prüfen
            if check_password_hash(user.password_hash, password):
                # Login erfolgreich - auch wenn Token abgelaufen ist
                # Die Projektzugriffsprüfung passiert in der index() Route via is_access_valid()
                login_user(user, remember=True)

                # Last login aktualisieren
                from app import db

                user.last_login = datetime.now()
                db.session.commit()

                # Warnung anzeigen wenn Token abgelaufen
                if user.token_expires and user.token_expires < datetime.now():
                    flash(
                        f"Willkommen, {user.name}! Ihr Token ist abgelaufen - Sie können ihn jederzeit selbst verlängern.",
                        "warning",
                    )
                else:
                    flash(f"Willkommen, {user.name}!", "success")

                return redirect(url_for("main.index"))
            else:
                flash("Ungültiges Passwort.", "error")
        else:
            flash("Kein aktiver Account mit dieser E-Mail-Adresse gefunden.", "error")

    return render_template(
        "auth/portfolio_login.html", contact=Contact.query.first(), now=datetime.now()
    )
