from flask import render_template, Blueprint, request, session, redirect, url_for, flash, jsonify
from datetime import datetime
from app.models import Certification, Contact, About, Project, GitHubProject, Skill, AccessRequest
from app.data import parse_date
from app import db
import secrets

main = Blueprint("main", __name__)


@main.route("/")
def index():
    # Prüfen ob ein gültiges Token in der Session vorhanden ist
    show_projects = False
    token = session.get('access_token')
    
    if token:
        access_request = AccessRequest.query.filter_by(token=token, status='approved').first()
        if access_request and (access_request.token_expires is None or access_request.token_expires > datetime.now()):
            show_projects = True
    
    projects = []
    github_projects = []
    
    if show_projects:
        projects = Project.query.all()
        github_projects = GitHubProject.query.all()
        projects = sorted(
            projects, key=lambda project: parse_date(project.bis), reverse=True
        )
    
    skills = Skill.query.all()
    about = About.query.first()
    contact = Contact.query.first()
    certifications = Certification.query.all()

    certifications = sorted(
        certifications, key=lambda cert: parse_date(cert.date), reverse=True
    )
    skills = sorted(skills, key=lambda skill: skill.name)

    return render_template(
        "main/index.html",
        projects=projects,
        github_projects=github_projects,
        about=about,
        contact=contact,
        skills=skills,
        certifications=certifications,
        now=datetime.now(),
        show_projects=show_projects,
    )


@main.route("/request-access", methods=["POST"])
def request_access():
    """Anfrage für Projektzugriff erstellen"""
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message', '')
    
    if not name or not email:
        flash('Bitte geben Sie Name und E-Mail-Adresse an.', 'error')
        return redirect(url_for('main.index'))
    
    # Neue Anfrage erstellen
    access_request = AccessRequest(
        name=name,
        email=email,
        message=message,
        status='pending'
    )
    
    db.session.add(access_request)
    db.session.commit()
    
    # E-Mail an Admin senden
    try:
        from app.email_utils import send_admin_notification
        send_admin_notification(access_request)
    except Exception as e:
        print(f"E-Mail konnte nicht gesendet werden: {e}")
    
    flash('Ihre Anfrage wurde erfolgreich gesendet. Sie erhalten in Kürze eine E-Mail mit dem Zugangstoken.', 'success')
    return redirect(url_for('main.index'))


@main.route("/validate-token", methods=["POST"])
def validate_token():
    """Token validieren und Zugriff gewähren"""
    token = request.form.get('token')
    
    if not token:
        flash('Bitte geben Sie ein Token ein.', 'error')
        return redirect(url_for('main.index'))
    
    access_request = AccessRequest.query.filter_by(token=token, status='approved').first()
    
    if access_request:
        if access_request.token_expires is None or access_request.token_expires > datetime.now():
            session['access_token'] = token
            flash('Zugriff gewährt! Sie können nun alle Projekte sehen.', 'success')
        else:
            flash('Dieses Token ist abgelaufen.', 'error')
    else:
        flash('Ungültiges Token.', 'error')
    
    return redirect(url_for('main.index'))


@main.route("/revoke-access")
def revoke_access():
    """Zugriff widerrufen (Token aus Session entfernen)"""
    session.pop('access_token', None)
    flash('Zugriff wurde widerrufen.', 'info')
    return redirect(url_for('main.index'))
