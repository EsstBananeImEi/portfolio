from datetime import datetime, timedelta
from flask import render_template, redirect, url_for, flash, request, jsonify, send_file
from flask_login import login_required
from app import db
from app.models import About, Contact, AccessRequest, TimelineItem
from app.forms import AboutForm
from app.admin import admin
import secrets
import json
from io import BytesIO


@admin.route("/about", methods=["GET", "POST"])
@login_required
def edit_about():
    # Nur echte Admins dürfen Bio bearbeiten
    from flask_login import current_user

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash(
            "Zugriff verweigert. Nur Administratoren dürfen die Bio bearbeiten.",
            "error",
        )
        return redirect(url_for("main.index"))

    # Wir nehmen an, dass es nur einen Datensatz gibt
    about = About.query.first()
    form = AboutForm(obj=about)

    if form.validate_on_submit():
        if about:
            # Datensatz aktualisieren
            form.populate_obj(about)
            flash("Bio wurde aktualisiert.", "success")
        else:
            # Datensatz erstellen
            about = About()
            form.populate_obj(about)
            db.session.add(about)
            flash("Bio wurde erstellt.", "success")
        db.session.commit()
        return redirect(url_for("admin.dashboard", active_tab="bio"))

    # Redirect to dashboard
    return redirect(url_for("admin.dashboard", active_tab="bio"))


@admin.route("/dashboard")
@login_required
def dashboard():
    """Zentrales Admin Dashboard mit Tabs"""
    from flask_login import current_user

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    # Daten für alle Tabs laden
    about = About.query.first()
    form = AboutForm(obj=about)

    timeline_items = (
        TimelineItem.query.filter_by(is_active=True)
        .order_by(TimelineItem.position)
        .all()
    )

    requests = AccessRequest.query.order_by(AccessRequest.created_at.desc()).all()

    active_tab = request.args.get("active_tab", "bio")

    return render_template(
        "admin/dashboard.html",
        form=form,
        about=about,
        timeline_items=timeline_items,
        requests=requests,
        active_tab=active_tab,
        contact=Contact.query.first(),
        now=datetime.now(),
    )


@admin.route("/about/delete", methods=["POST"])
@login_required
def delete_about():
    # Nur echte Admins
    from flask_login import current_user

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    about = About.query.first()
    if about:
        db.session.delete(about)
        db.session.commit()
        flash("Bio wurde gelöscht.", "success")
    else:
        flash("Kein Bio-Datensatz gefunden.", "error")
    return redirect(url_for("admin.dashboard", active_tab="bio"))


@admin.route("/stats", methods=["GET", "POST"])
@login_required
def edit_stats():
    """Statistiken & Highlights bearbeiten (Demo-Route)"""
    # Nur echte Admins
    from flask_login import current_user

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    # TODO: Hier würde die Logik zum Speichern/Laden kommen
    return render_template(
        "admin/edit_stats.html",
        contact=Contact.query.first(),
        now=datetime.now(),
    )


@admin.route("/access-requests")
@login_required
def access_requests():
    """Liste aller Zugriffsanfragen - Redirect zum Dashboard"""
    return redirect(url_for("admin.dashboard", active_tab="access"))


@admin.route("/access-requests/<int:request_id>/generate-token", methods=["POST"])
@login_required
def generate_token(request_id):
    """User-Account für eine Anfrage erstellen und Zugangsdaten generieren"""
    from werkzeug.security import generate_password_hash
    from flask_login import current_user

    # Nur echte Admins
    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    access_request = AccessRequest.query.get_or_404(request_id)

    # Generiere ein sicheres Passwort (16 Zeichen)
    password = secrets.token_urlsafe(16)

    # Token generieren (32 Bytes = 64 Zeichen Hex) - wird noch für Kompatibilität behalten
    token = secrets.token_hex(32)

    # Token-Ablaufdatum (optional, z.B. 90 Tage)
    expires_days = request.form.get("expires_days", type=int)
    if expires_days and expires_days > 0:
        token_expires = datetime.now() + timedelta(days=expires_days)
    else:
        token_expires = None  # Kein Ablaufdatum

    # User-Account aktivieren
    access_request.token = token
    access_request.token_expires = token_expires
    access_request.status = "approved"
    access_request.password_hash = generate_password_hash(password)
    access_request.is_active = True

    db.session.commit()

    # Zugangsdaten per E-Mail an den Benutzer senden
    try:
        from app.email_utils import send_access_credentials

        if send_access_credentials(access_request, password):
            flash(
                f"Zugangsdaten wurden erstellt und per E-Mail an {access_request.email} gesendet!",
                "success",
            )
        else:
            flash(
                f"Zugangsdaten erstellt. E-Mail: {access_request.email}, Passwort: {password} (E-Mail konnte nicht gesendet werden)",
                "warning",
            )
    except Exception as e:
        print(f"Fehler beim E-Mail-Versand: {e}")
        flash(
            f"Zugangsdaten erstellt. E-Mail: {access_request.email}, Passwort: {password} (E-Mail-Versand fehlgeschlagen)",
            "warning",
        )

    return redirect(url_for("admin.dashboard", active_tab="access"))


@admin.route("/access-requests/<int:request_id>/revoke", methods=["POST"])
@login_required
def revoke_token(request_id):
    """Zugriff widerrufen und Account deaktivieren"""
    from flask_login import current_user

    # Nur echte Admins
    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    access_request = AccessRequest.query.get_or_404(request_id)

    access_request.status = "rejected"
    access_request.token = None
    access_request.token_expires = None
    access_request.is_active = False  # Account deaktivieren

    db.session.commit()

    flash("Zugriff wurde widerrufen und Account deaktiviert.", "success")
    return redirect(url_for("admin.dashboard", active_tab="access"))


@admin.route("/access-requests/<int:request_id>/delete", methods=["POST"])
@login_required
def delete_request(request_id):
    """Anfrage löschen"""
    from flask_login import current_user

    # Nur echte Admins
    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    access_request = AccessRequest.query.get_or_404(request_id)

    db.session.delete(access_request)
    db.session.commit()

    flash("Anfrage wurde gelöscht.", "success")
    return redirect(url_for("admin.dashboard", active_tab="access"))


@admin.route("/timeline")
@login_required
def edit_timeline():
    """Timeline bearbeiten - Redirect zum Dashboard"""
    return redirect(url_for("admin.dashboard", active_tab="timeline"))


@admin.route("/timeline/<int:item_id>/update", methods=["POST"])
@login_required
def update_timeline_item(item_id):
    """Timeline-Eintrag aktualisieren"""
    from flask_login import current_user

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    item = TimelineItem.query.get_or_404(item_id)

    item.period_start = request.form.get("period_start")
    item.period_end = request.form.get("period_end")
    item.title = request.form.get("title")
    item.company = request.form.get("company")
    item.description = request.form.get("description")
    item.badge = request.form.get("badge")
    item.badge_color = request.form.get("badge_color")
    item.icon_type = request.form.get("icon_type")
    item.position = request.form.get("position", type=int)
    item.tags = request.form.get("tags")

    db.session.commit()
    flash("Timeline-Eintrag wurde aktualisiert.", "success")
    return redirect(url_for("admin.dashboard", active_tab="timeline"))


@admin.route("/timeline/<int:item_id>/delete")
@login_required
def delete_timeline_item(item_id):
    """Timeline-Eintrag löschen"""
    from flask_login import current_user

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    item = TimelineItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()

    flash("Timeline-Eintrag wurde gelöscht.", "success")
    return redirect(url_for("admin.dashboard", active_tab="timeline"))


@admin.route("/timeline/add", methods=["GET", "POST"])
@login_required
def add_timeline_item():
    """Neuer Timeline-Eintrag erstellen"""
    from flask_login import current_user

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    if request.method == "POST":
        # Neuen Eintrag erstellen
        new_item = TimelineItem(
            position=request.form.get("position", type=int),
            period_start=request.form.get("period_start"),
            period_end=request.form.get("period_end"),
            title=request.form.get("title"),
            company=request.form.get("company"),
            description=request.form.get("description"),
            badge=request.form.get("badge"),
            badge_color=request.form.get("badge_color", "primary"),
            icon_type=request.form.get("icon_type", "microsoft"),
            tags=request.form.get("tags"),
            is_active=True,
        )

        db.session.add(new_item)
        db.session.commit()

        flash("Neuer Timeline-Eintrag wurde erstellt.", "success")
        return redirect(url_for("admin.dashboard", active_tab="timeline"))

    # GET: Formular anzeigen
    # Nächste Position ermitteln
    max_position = db.session.query(db.func.max(TimelineItem.position)).scalar() or 0
    next_position = max_position + 1

    return render_template(
        "admin/add_timeline.html",
        next_position=next_position,
        contact=Contact.query.first(),
        now=datetime.now(),
    )


@admin.route("/export/all")
@login_required
def export_all_data():
    """Exportiert alle Daten als JSON"""
    from flask_login import current_user
    import os

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    # Sammle alle Daten
    data = {
        "bio": {},
        "timeline": [],
        "projects": [],
        "github_projects": [],
        "skills": [],
        "certs": [],
        "contact": {},
        "access_requests": [],
        "exported_at": datetime.now().isoformat(),
    }

    # Bio
    about = About.query.first()
    if about:
        data["bio"] = {
            "name": about.name,
            "title": about.title,
            "description": about.description,
            "image": about.image,
        }

    # Timeline
    timeline_items = TimelineItem.query.order_by(TimelineItem.position).all()
    for item in timeline_items:
        data["timeline"].append(
            {
                "id": item.id,
                "title": item.title,
                "organization": item.organization,
                "date": item.date,
                "description": item.description,
                "icon": item.icon,
                "position": item.position,
                "is_active": item.is_active,
            }
        )

    # Contact
    contact = Contact.query.first()
    if contact:
        data["contact"] = {
            "email": contact.email,
            "phone": contact.phone,
            "location": contact.location,
            "github": contact.github,
            "linkedin": contact.linkedin,
            "twitter": contact.twitter,
        }

    # Access Requests
    requests = AccessRequest.query.all()
    for req in requests:
        data["access_requests"].append(
            {
                "id": req.id,
                "email": req.email,
                "created_at": req.created_at.isoformat() if req.created_at else None,
                "expires_at": req.expires_at.isoformat() if req.expires_at else None,
                "is_used": req.is_used,
            }
        )

    # JSON-Daten aus Dateien lesen
    from pathlib import Path

    data_dir = Path(__file__).parent.parent / "data"

    json_files = {
        "projects": "projects.json",
        "github_projects": "github_projects.json",
        "skills": "skills.json",
        "certs": "certs.json",
    }

    for key, filename in json_files.items():
        file_path = data_dir / filename
        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data[key] = json.load(f)
            except Exception as e:
                data[key] = {"error": str(e)}

    # JSON erstellen
    json_data = json.dumps(data, ensure_ascii=False, indent=2)

    # Als Datei zurückgeben
    buffer = BytesIO()
    buffer.write(json_data.encode("utf-8"))
    buffer.seek(0)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"portfolio_backup_{timestamp}.json"

    return send_file(
        buffer, mimetype="application/json", as_attachment=True, download_name=filename
    )


@admin.route("/export/<data_type>")
@login_required
def export_data(data_type):
    """Exportiert spezifische Daten als JSON"""
    from flask_login import current_user
    from pathlib import Path

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    data = {"type": data_type, "exported_at": datetime.now().isoformat()}

    if data_type == "bio":
        about = About.query.first()
        if about:
            data["data"] = {
                "name": about.name,
                "title": about.title,
                "description": about.description,
                "image": about.image,
            }

    elif data_type == "timeline":
        timeline_items = TimelineItem.query.order_by(TimelineItem.position).all()
        data["data"] = []
        for item in timeline_items:
            data["data"].append(
                {
                    "id": item.id,
                    "title": item.title,
                    "organization": item.organization,
                    "date": item.date,
                    "description": item.description,
                    "icon": item.icon,
                    "position": item.position,
                    "is_active": item.is_active,
                }
            )

    elif data_type == "contact":
        contact = Contact.query.first()
        if contact:
            data["data"] = {
                "email": contact.email,
                "phone": contact.phone,
                "location": contact.location,
                "github": contact.github,
                "linkedin": contact.linkedin,
                "twitter": contact.twitter,
            }

    elif data_type == "access_requests":
        requests = AccessRequest.query.all()
        data["data"] = []
        for req in requests:
            data["data"].append(
                {
                    "id": req.id,
                    "email": req.email,
                    "created_at": (
                        req.created_at.isoformat() if req.created_at else None
                    ),
                    "expires_at": (
                        req.expires_at.isoformat() if req.expires_at else None
                    ),
                    "is_used": req.is_used,
                }
            )

    elif data_type in ["projects", "github_projects", "skills", "certs"]:
        # JSON-Datei lesen
        data_dir = Path(__file__).parent.parent / "data"
        json_files = {
            "projects": "projects.json",
            "github_projects": "github_projects.json",
            "skills": "skills.json",
            "certs": "certs.json",
        }

        file_path = data_dir / json_files[data_type]
        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data["data"] = json.load(f)
            except Exception as e:
                data["data"] = {"error": str(e)}
        else:
            data["data"] = {"error": "File not found"}

    else:
        flash("Ungültiger Datentyp.", "error")
        return redirect(url_for("admin.dashboard", active_tab="backup"))

    # JSON erstellen
    json_data = json.dumps(data, ensure_ascii=False, indent=2)

    # Als Datei zurückgeben
    buffer = BytesIO()
    buffer.write(json_data.encode("utf-8"))
    buffer.seek(0)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"portfolio_{data_type}_{timestamp}.json"

    return send_file(
        buffer, mimetype="application/json", as_attachment=True, download_name=filename
    )
