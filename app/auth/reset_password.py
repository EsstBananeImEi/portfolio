from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    current_app,
)
from app.models import AccessRequest
from app.email_utils import send_access_credentials
from werkzeug.security import generate_password_hash
import secrets

reset = Blueprint("reset", __name__)


@reset.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    from app.models import Contact
    from datetime import datetime

    contact = Contact.query.first()
    now = datetime.now()
    if request.method == "POST":
        email = request.form.get("email")
        if not email:
            flash("Bitte geben Sie Ihre E-Mail-Adresse ein.", "error")
            return render_template(
                "auth/forgot_password.html", contact=contact, now=now
            )
        user = AccessRequest.query.filter_by(
            email=email, is_active=True, status="approved"
        ).first()
        if not user:
            flash("Kein aktiver Benutzer mit dieser E-Mail-Adresse gefunden.", "error")
            return render_template(
                "auth/forgot_password.html", contact=contact, now=now
            )
        # Neues Passwort generieren
        new_password = secrets.token_urlsafe(10)
        user.password_hash = generate_password_hash(new_password)
        from app import db

        db.session.commit()
        from app.email_utils import send_password_reset_email

        send_password_reset_email(user, new_password)
        flash("Ein neues Passwort wurde an Ihre E-Mail-Adresse gesendet.", "success")
        return redirect(url_for("auth.portfolio_login"))
    return render_template("auth/forgot_password.html", contact=contact, now=now)
