from datetime import datetime, timedelta
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required
from app import db
from app.models import About, Contact, AccessRequest
from app.forms import AboutForm
from app.admin import admin
import secrets


@admin.route("/about", methods=["GET", "POST"])
@login_required
def edit_about():
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
    about = About.query.first()
    if about:
        db.session.delete(about)
        db.session.commit()
        flash("Bio wurde gelöscht.", "success")
    else:
        flash("Kein Bio-Datensatz gefunden.", "error")
    return redirect(url_for("admin.edit_about"))


@admin.route("/access-requests")
@login_required
def access_requests():
    """Liste aller Zugriffsanfragen"""
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
    """Token für eine Anfrage generieren"""
    access_request = AccessRequest.query.get_or_404(request_id)
    
    # Token generieren (32 Bytes = 64 Zeichen Hex)
    token = secrets.token_hex(32)
    
    # Token-Ablaufdatum (optional, z.B. 90 Tage)
    expires_days = request.form.get('expires_days', type=int)
    if expires_days and expires_days > 0:
        token_expires = datetime.now() + timedelta(days=expires_days)
    else:
        token_expires = None  # Kein Ablaufdatum
    
    access_request.token = token
    access_request.token_expires = token_expires
    access_request.status = 'approved'
    
    db.session.commit()
    
    # Token automatisch per E-Mail an den Benutzer senden
    try:
        from app.email_utils import send_token_email
        if send_token_email(access_request):
            flash(f'Token wurde generiert und per E-Mail an {access_request.email} gesendet!', 'success')
        else:
            flash(f'Token wurde generiert: {token} (E-Mail konnte nicht gesendet werden)', 'warning')
    except Exception as e:
        print(f"Fehler beim E-Mail-Versand: {e}")
        flash(f'Token wurde generiert: {token} (E-Mail-Versand fehlgeschlagen)', 'warning')
    
    return redirect(url_for('admin.access_requests'))


@admin.route("/access-requests/<int:request_id>/revoke", methods=["POST"])
@login_required
def revoke_token(request_id):
    """Token widerrufen"""
    access_request = AccessRequest.query.get_or_404(request_id)
    
    access_request.status = 'rejected'
    access_request.token = None
    access_request.token_expires = None
    
    db.session.commit()
    
    flash('Token wurde widerrufen.', 'success')
    return redirect(url_for('admin.access_requests'))


@admin.route("/access-requests/<int:request_id>/delete", methods=["POST"])
@login_required
def delete_request(request_id):
    """Anfrage löschen"""
    access_request = AccessRequest.query.get_or_404(request_id)
    
    db.session.delete(access_request)
    db.session.commit()
    
    flash('Anfrage wurde gelöscht.', 'success')
    return redirect(url_for('admin.access_requests'))
