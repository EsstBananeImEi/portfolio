from datetime import datetime, timedelta
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required
from app import db
from app.models import About, Contact, AccessRequest, TimelineItem
from app.forms import AboutForm
from app.admin import admin
import secrets


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
        return redirect(url_for("admin.edit_about"))

    return render_template(
        "admin/edit_about.html",
        form=form,
        about=about,
        now=datetime.now(),
        contact=Contact.query.first(),
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
    return redirect(url_for("admin.edit_about"))


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
    """Liste aller Zugriffsanfragen"""
    # Nur echte Admins
    from flask_login import current_user

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash(
            "Zugriff verweigert. Nur Administratoren dürfen Zugriffsanfragen verwalten.",
            "error",
        )
        return redirect(url_for("main.index"))

    requests = AccessRequest.query.order_by(AccessRequest.created_at.desc()).all()
    return render_template(
        "admin/access_requests.html",
        requests=requests,
        now=datetime.now(),
        contact=Contact.query.first(),
    )


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

    return redirect(url_for("admin.access_requests"))


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
    return redirect(url_for("admin.access_requests"))


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
    return redirect(url_for("admin.access_requests"))


@admin.route("/timeline")
@login_required
def edit_timeline():
    """Timeline bearbeiten"""
    from flask_login import current_user

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    timeline_items = (
        TimelineItem.query.filter_by(is_active=True)
        .order_by(TimelineItem.position)
        .all()
    )
    return render_template(
        "admin/edit_timeline.html",
        timeline_items=timeline_items,
        contact=Contact.query.first(),
        now=datetime.now(),
    )


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
    return redirect(url_for("admin.edit_timeline"))


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
    return redirect(url_for("admin.edit_timeline"))


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
        return redirect(url_for("admin.edit_timeline"))

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
