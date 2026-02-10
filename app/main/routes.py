from flask import (
    render_template,
    Blueprint,
    request,
    session,
    redirect,
    url_for,
    flash,
    jsonify,
)
from datetime import datetime
from flask_login import current_user
from app.models import (
    Certification,
    Contact,
    About,
    Project,
    GitHubProject,
    Skill,
    AccessRequest,
    TimelineItem,
)
from app.data import parse_date
from app import db
import secrets

main = Blueprint("main", __name__)


@main.route("/")
def index():
    # Prüfen ob Benutzer eingeloggt ist
    show_projects = False

    # Portfolio-User eingeloggt?
    if current_user.is_authenticated:
        # Admin hat immer Zugriff
        if hasattr(current_user, "get_id") and current_user.get_id() == "1":
            show_projects = True
        # Portfolio-User: Prüfe ob es ein AccessRequest-Objekt ist
        elif isinstance(current_user, AccessRequest):
            if current_user.is_access_valid():
                show_projects = True

    # Fallback: Token-basierter Zugriff (für Abwärtskompatibilität)
    if not show_projects:
        token = session.get("access_token")
        if token:
            access_request = AccessRequest.query.filter_by(
                token=token, status="approved"
            ).first()
            if access_request and (
                access_request.token_expires is None
                or access_request.token_expires > datetime.now()
            ):
                show_projects = True

    projects = []

    if show_projects:
        projects = Project.query.all()
        projects = sorted(
            projects, key=lambda project: parse_date(project.bis), reverse=True
        )

    # GitHub-Projekte sind immer sichtbar (nicht geschützt)
    github_projects = GitHubProject.query.all()

    skills = Skill.query.all()
    about = About.query.first()
    contact = Contact.query.first()
    certifications = Certification.query.all()

    certifications = sorted(
        certifications, key=lambda cert: parse_date(cert.date), reverse=True
    )
    skills = sorted(skills, key=lambda skill: skill.name)

    # Statistiken berechnen
    def calculate_experience_years(project_type):
        """Berechnet Jahre Erfahrung basierend auf Projekt-Typen"""
        import math

        # Nur reguläre Projekte, keine GitHub-Projekte
        all_projects = list(Project.query.all())
        total_months = 0

        for project in all_projects:
            # Prüfe ob Projekt den gewünschten Typ hat
            if hasattr(project, "types") and project.types:
                project_types = [t.strip() for t in project.types.split(",")]
                if project_type not in project_types:
                    continue
            else:
                continue

            # Parse Datumsangaben
            try:
                von = parse_date(project.von)
                bis = parse_date(project.bis)
                if von and bis:
                    # Berechne Monate zwischen zwei Daten
                    months_diff = (bis.year - von.year) * 12 + (bis.month - von.month)
                    total_months += months_diff
            except:
                continue

        if total_months > 0:
            years = total_months / 12
            # Runde auf nächste 0.5er Stelle nach unten (4.8 → 4.5, 8.2 → 8.0)
            rounded = math.floor(years * 2) / 2
            return rounded if rounded > 0 else 0.5
        return 0

    stats = {
        "years_dynamics": calculate_experience_years("dynamics"),
        "years_software": calculate_experience_years("software"),
        "total_projects": (lambda count: (count // 5) * 5 if count >= 5 else count)(
            Project.query.count()
        ),
        "total_skills": (lambda count: (count // 5) * 5 if count >= 5 else count)(
            Skill.query.count()
        ),
    }

    # Timeline-Daten laden
    timeline_items = (
        TimelineItem.query.filter_by(is_active=True)
        .order_by(getattr(TimelineItem, "position"))
        .all()
    )

    # Timeline nur für authentifizierte Benutzer anzeigen
    show_timeline = current_user.is_authenticated

    return render_template(
        "main/index.html",
        projects=projects,
        github_projects=github_projects,
        about=about,
        contact=contact,
        skills=skills,
        certifications=certifications,
        timeline_items=timeline_items,
        now=datetime.now(),
        show_projects=show_projects,
        show_timeline=show_timeline,
        stats=stats,
    )


@main.route("/request-access", methods=["POST"])
def request_access():
    """Anfrage für Projektzugriff erstellen"""
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message", "")

    if not name or not email:
        flash("Bitte geben Sie Name und E-Mail-Adresse an.", "error")
        return redirect(url_for("main.index"))

    # Neue Anfrage erstellen
    access_request = AccessRequest(
        name=name, email=email, message=message, status="pending"
    )

    db.session.add(access_request)
    db.session.commit()

    # E-Mail an Admin senden
    try:
        from app.email_utils import send_admin_notification

        send_admin_notification(access_request)
    except Exception as e:
        print(f"E-Mail konnte nicht gesendet werden: {e}")

    flash(
        "Ihre Anfrage wurde erfolgreich gesendet. Sie erhalten in Kürze eine E-Mail mit dem Zugangstoken.",
        "success",
    )
    return redirect(url_for("main.index"))


@main.route("/validate-token", methods=["POST"])
def validate_token():
    """Token validieren und Zugriff gewähren"""
    token = request.form.get("token")

    if not token:
        flash("Bitte geben Sie ein Token ein.", "error")
        return redirect(url_for("main.index"))

    access_request = AccessRequest.query.filter_by(
        token=token, status="approved"
    ).first()

    if access_request:
        if (
            access_request.token_expires is None
            or access_request.token_expires > datetime.now()
        ):
            session["access_token"] = token
            flash("Zugriff gewährt! Sie können nun alle Projekte sehen.", "success")
        else:
            flash("Dieses Token ist abgelaufen.", "error")
    else:
        flash("Ungültiges Token.", "error")

    return redirect(url_for("main.index"))


@main.route("/revoke-access")
def revoke_access():
    """Zugriff widerrufen (Token aus Session entfernen oder User ausloggen)"""
    from flask_login import logout_user

    # Wenn User eingeloggt ist, ausloggen
    if current_user.is_authenticated and isinstance(current_user, AccessRequest):
        logout_user()
        flash("Sie wurden abgemeldet.", "info")
    else:
        # Andernfalls nur Token entfernen
        session.pop("access_token", None)
        flash("Zugriff wurde widerrufen.", "info")

    return redirect(url_for("main.index"))


@main.route("/revoke-access-keep-account", methods=["POST"])
def revoke_access_keep_account():
    """Zugriff widerrufen, aber Account und Login behalten"""
    # Nur eingeloggte Portfolio-User
    if not current_user.is_authenticated or not isinstance(current_user, AccessRequest):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    # Admin kann dies nicht tun
    if hasattr(current_user, "get_id") and current_user.get_id() == "1":
        flash("Diese Funktion ist nicht für Administratoren verfügbar.", "error")
        return redirect(url_for("main.index"))

    try:
        from datetime import timedelta

        # Account behalten, User eingeloggt lassen, aber Token abgelaufen setzen
        # is_active bleibt True, damit User sich wieder einloggen kann
        # token_expires wird auf ein vergangenes Datum gesetzt → kein Projektzugriff
        current_user.token_expires = datetime.now() - timedelta(days=1)
        db.session.commit()

        flash(
            f"Zugriff wurde widerrufen. Sie bleiben eingeloggt, können aber keine Projekte mehr sehen. Sie können Ihren Token jederzeit verlängern.",
            "warning",
        )
    except Exception as e:
        db.session.rollback()
        flash(f"Fehler beim Widerrufen des Zugriffs: {str(e)}", "error")

    return redirect(url_for("main.index"))


@main.route("/renew-token")
def renew_token():
    """Portfolio-User kann seinen Token selbst um 3 Tage verlängern"""
    from datetime import timedelta

    # Nur eingeloggte Portfolio-User
    if not current_user.is_authenticated or not isinstance(current_user, AccessRequest):
        flash("Bitte melden Sie sich an, um Ihren Token zu verlängern.", "error")
        return redirect(url_for("auth.portfolio_login"))

    # Admin kann dies nicht tun
    if hasattr(current_user, "get_id") and current_user.get_id() == "1":
        flash("Diese Funktion ist nicht für Administratoren verfügbar.", "error")
        return redirect(url_for("main.index"))

    try:
        user_id = current_user.id
        access_request = AccessRequest.query.get(user_id)

        if access_request:
            # Token um 3 Tage verlängern ab jetzt
            new_expiry = datetime.now() + timedelta(days=3)
            access_request.token_expires = new_expiry
            access_request.is_active = True
            access_request.status = "approved"

            db.session.commit()

            flash(
                f"Ihr Token wurde erfolgreich verlängert bis {new_expiry.strftime('%d.%m.%Y %H:%M')} Uhr.",
                "success",
            )
        else:
            flash("Account nicht gefunden.", "error")
    except Exception as e:
        db.session.rollback()
        flash(f"Fehler beim Verlängern des Tokens: {str(e)}", "error")

    return redirect(url_for("main.index"))


@main.route("/delete-account", methods=["POST"])
def delete_account():
    """Portfolio-User kann seinen eigenen Account löschen"""
    from flask_login import logout_user, login_required

    # Nur eingeloggte Portfolio-User
    if not current_user.is_authenticated or not isinstance(current_user, AccessRequest):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    # Admin kann sich nicht selbst löschen
    if hasattr(current_user, "get_id") and current_user.get_id() == "1":
        flash("Admin-Account kann nicht gelöscht werden.", "error")
        return redirect(url_for("main.index"))

    # User-Daten speichern vor Logout
    user_name = current_user.name
    user_id = current_user.id

    # User ausloggen
    logout_user()

    # Account aus Datenbank löschen
    try:
        access_request = AccessRequest.query.get(user_id)
        if access_request:
            db.session.delete(access_request)
            db.session.commit()
            flash(f"Account von {user_name} wurde erfolgreich gelöscht.", "success")
        else:
            flash("Account nicht gefunden.", "error")
    except Exception as e:
        db.session.rollback()
        flash(f"Fehler beim Löschen des Accounts: {str(e)}", "error")

    return redirect(url_for("main.index"))
