from datetime import datetime, timedelta
from flask import render_template, redirect, url_for, flash, request, jsonify, send_file
from flask_login import login_required
from app import db
from app.models import About, Contact, AccessRequest, TimelineItem, Certification
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
    from pathlib import Path

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    # Daten für alle Tabs laden
    about = About.query.first()
    form = AboutForm(obj=about)

    timeline_items = (
        TimelineItem.query.filter_by(is_active=True)
        .order_by(getattr(TimelineItem, "position"))
        .all()
    )

    requests = AccessRequest.query.order_by(AccessRequest.created_at.desc()).all()

    # Projekte und Skills laden
    data_dir = Path(__file__).parent.parent / "data"
    portfolio_projects = []
    github_projects = []
    skills = []
    certs = []

    try:
        with open(data_dir / "projects.json", "r", encoding="utf-8") as f:
            portfolio_projects = json.load(f)
    except Exception as e:
        flash(f"Fehler beim Laden der Portfolio-Projekte: {str(e)}", "error")

    try:
        with open(data_dir / "github_projects.json", "r", encoding="utf-8") as f:
            github_projects = json.load(f)
    except Exception as e:
        flash(f"Fehler beim Laden der GitHub-Projekte: {str(e)}", "error")

    try:
        with open(data_dir / "skills.json", "r", encoding="utf-8") as f:
            skills = json.load(f)
    except Exception as e:
        flash(f"Fehler beim Laden der Skills: {str(e)}", "error")

    try:
        with open(data_dir / "certs.json", "r", encoding="utf-8") as f:
            certs = json.load(f)
    except Exception as e:
        flash(f"Fehler beim Laden der Zertifikate: {str(e)}", "error")

    # Certifications laden
    certifications = Certification.query.order_by(
        getattr(Certification, "date").desc()
    ).all()

    # Backup-Tab: Statistiken
    bio_count = 1 if about else 0
    timeline_count = len(timeline_items)
    access_count = len(requests)
    projects_count = len(portfolio_projects)
    github_count = len(github_projects)
    skills_count = len(skills)
    certs_count = len(certs)

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
        portfolio_projects=portfolio_projects,
        github_projects=github_projects,
        skills=skills,
        certifications=certifications,
        # Backup-Tab Statistiken
        bio_count=bio_count,
        timeline_count=timeline_count,
        access_count=access_count,
        projects_count=projects_count,
        github_count=github_count,
        skills_count=skills_count,
        certs_count=certs_count,
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
    max_position = (
        db.session.query(db.func.max(getattr(TimelineItem, "position"))).scalar() or 0
    )
    next_position = max_position + 1

    return render_template(
        "admin/add_timeline.html",
        next_position=next_position,
        contact=Contact.query.first(),
        now=datetime.now(),
    )


# ========== PORTFOLIO PROJECTS ROUTES ==========


@admin.route("/projects/portfolio/add", methods=["POST"])
@login_required
def add_portfolio_project():
    """Portfolio-Projekt hinzufügen"""
    from flask_login import current_user
    from pathlib import Path
    from app.models import Project, Task

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    data_dir = Path(__file__).parent.parent / "data"
    projects_file = data_dir / "projects.json"

    # Projekte laden
    try:
        with open(projects_file, "r", encoding="utf-8") as f:
            projects = json.load(f)
    except Exception:
        projects = []

    # Aufgaben verarbeiten (eine pro Zeile)
    aufgaben_text = request.form.get("aufgaben", "").strip()
    aufgaben = (
        [line.strip() for line in aufgaben_text.split("\n") if line.strip()]
        if aufgaben_text
        else []
    )

    # Neues Projekt erstellen
    new_project = {
        "title": request.form.get("title"),
        "shortDescription": request.form.get("shortDescription"),
        "rolle": request.form.get("rolle", ""),
        "description": request.form.get("description"),
        "aufgaben": aufgaben,
        "technologien": request.form.get("technologien", ""),
        "von": request.form.get("von", ""),
        "bis": request.form.get("bis", ""),
        "logo": request.form.get("logo", ""),
        "link": request.form.get("link", ""),
        "types": request.form.get("types", ""),
    }

    projects.append(new_project)

    # In JSON-Datei speichern
    try:
        with open(projects_file, "w", encoding="utf-8") as f:
            json.dump(projects, f, ensure_ascii=False, indent=4)

        # In Datenbank speichern
        db_project = Project(
            title=new_project["title"],
            shortDescription=new_project["shortDescription"],
            rolle=new_project["rolle"],
            description=new_project["description"],
            technologien=new_project["technologien"],
            von=new_project["von"],
            bis=new_project["bis"],
            logo=new_project["logo"],
            link=new_project["link"],
            types=new_project["types"],
        )
        db.session.add(db_project)
        db.session.flush()  # Um die ID zu bekommen

        # Tasks hinzufügen
        for aufgabe in aufgaben:
            task = Task(description=aufgabe, project_id=db_project.id)
            db.session.add(task)

        db.session.commit()
        flash("Portfolio-Projekt wurde hinzugefügt.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Fehler beim Speichern: {str(e)}", "error")

    return redirect(url_for("admin.dashboard", active_tab="projects"))


@admin.route("/projects/portfolio/<int:project_id>/edit", methods=["POST"])
@login_required
def edit_portfolio_project(project_id):
    """Portfolio-Projekt bearbeiten"""
    from flask_login import current_user
    from pathlib import Path
    from app.models import Project, Task

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    data_dir = Path(__file__).parent.parent / "data"
    projects_file = data_dir / "projects.json"

    try:
        with open(projects_file, "r", encoding="utf-8") as f:
            projects = json.load(f)

        if 0 <= project_id < len(projects):
            # Aufgaben verarbeiten (eine pro Zeile)
            aufgaben_text = request.form.get("aufgaben", "").strip()
            aufgaben = (
                [line.strip() for line in aufgaben_text.split("\n") if line.strip()]
                if aufgaben_text
                else []
            )

            # Projekt aktualisieren
            projects[project_id] = {
                "title": request.form.get("title"),
                "shortDescription": request.form.get("shortDescription"),
                "rolle": request.form.get("rolle", ""),
                "description": request.form.get("description"),
                "aufgaben": aufgaben,
                "technologien": request.form.get("technologien", ""),
                "von": request.form.get("von", ""),
                "bis": request.form.get("bis", ""),
                "logo": request.form.get("logo", ""),
                "link": request.form.get("link", ""),
                "types": request.form.get("types", ""),
            }

            # In JSON speichern
            with open(projects_file, "w", encoding="utf-8") as f:
                json.dump(projects, f, ensure_ascii=False, indent=4)

            # Datenbank synchronisieren: Alle löschen und neu laden
            Task.query.delete()
            Project.query.delete()
            db.session.commit()

            # Alle Projekte aus JSON neu in DB laden
            for proj_data in projects:
                aufgaben = proj_data.get("aufgaben", [])
                db_project = Project(
                    title=proj_data.get("title", ""),
                    shortDescription=proj_data.get("shortDescription", ""),
                    rolle=proj_data.get("rolle", ""),
                    description=proj_data.get("description", ""),
                    technologien=proj_data.get("technologien", ""),
                    von=proj_data.get("von", ""),
                    bis=proj_data.get("bis", ""),
                    logo=proj_data.get("logo", ""),
                    link=proj_data.get("link", ""),
                    types=proj_data.get("types", ""),
                )
                db.session.add(db_project)
                db.session.flush()

                for aufgabe in aufgaben:
                    task = Task(description=aufgabe, project_id=db_project.id)
                    db.session.add(task)

            db.session.commit()
            flash("Portfolio-Projekt wurde aktualisiert.", "success")
        else:
            flash("Projekt nicht gefunden.", "error")
    except Exception as e:
        db.session.rollback()
        flash(f"Fehler beim Aktualisieren: {str(e)}", "error")

    return redirect(url_for("admin.dashboard", active_tab="projects"))


@admin.route("/projects/portfolio/<int:project_id>/delete", methods=["POST"])
@login_required
def delete_portfolio_project(project_id):
    """Portfolio-Projekt löschen"""
    from flask_login import current_user
    from pathlib import Path
    from app.models import Project, Task

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    data_dir = Path(__file__).parent.parent / "data"
    projects_file = data_dir / "projects.json"

    try:
        with open(projects_file, "r", encoding="utf-8") as f:
            projects = json.load(f)

        if 0 <= project_id < len(projects):
            deleted_project = projects.pop(project_id)

            with open(projects_file, "w", encoding="utf-8") as f:
                json.dump(projects, f, ensure_ascii=False, indent=4)

            # Datenbank synchronisieren: Alle löschen und neu laden
            Task.query.delete()
            Project.query.delete()
            db.session.commit()

            # Alle Projekte aus JSON neu in DB laden
            for proj_data in projects:
                aufgaben = proj_data.pop("aufgaben", [])
                db_project = Project(
                    title=proj_data.get("title", ""),
                    shortDescription=proj_data.get("shortDescription", ""),
                    rolle=proj_data.get("rolle", ""),
                    description=proj_data.get("description", ""),
                    technologien=proj_data.get("technologien", ""),
                    von=proj_data.get("von", ""),
                    bis=proj_data.get("bis", ""),
                    logo=proj_data.get("logo", ""),
                    link=proj_data.get("link", ""),
                    types=proj_data.get("types", ""),
                )
                db.session.add(db_project)
                db.session.flush()

                for aufgabe in aufgaben:
                    task = Task(description=aufgabe, project_id=db_project.id)
                    db.session.add(task)

            db.session.commit()
            flash(
                f"Projekt '{deleted_project.get('title', '')}' wurde gelöscht.",
                "success",
            )
        else:
            flash("Projekt nicht gefunden.", "error")
    except Exception as e:
        db.session.rollback()
        flash(f"Fehler beim Löschen: {str(e)}", "error")

    return redirect(url_for("admin.dashboard", active_tab="projects"))


# ========== GITHUB PROJECTS ROUTES ==========


@admin.route("/projects/github/add", methods=["POST"])
@login_required
def add_github_project():
    """GitHub-Projekt hinzufügen"""
    from flask_login import current_user
    from pathlib import Path
    from app.models import GitHubProject

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    data_dir = Path(__file__).parent.parent / "data"
    projects_file = data_dir / "github_projects.json"

    # Projekte laden
    try:
        with open(projects_file, "r", encoding="utf-8") as f:
            projects = json.load(f)
    except Exception:
        projects = []

    # Neues Projekt erstellen
    new_project = {
        "title": request.form.get("title"),
        "shortDescription": request.form.get("shortDescription"),
        "description": request.form.get("description"),
        "link": request.form.get("link"),
        "technologien": request.form.get("technologien", ""),
        "logo": request.form.get("logo", ""),
        "wip": request.form.get("wip") == "true",
    }

    projects.append(new_project)

    # In JSON-Datei speichern
    try:
        with open(projects_file, "w", encoding="utf-8") as f:
            json.dump(projects, f, ensure_ascii=False, indent=4)

        # In Datenbank speichern
        db_project = GitHubProject(
            title=new_project["title"],
            shortDescription=new_project["shortDescription"],
            types=new_project.get("types", ""),
            description=new_project["description"],
            link=new_project["link"],
            technologien=new_project["technologien"],
            logo=new_project["logo"],
            wip=new_project["wip"],
        )
        db.session.add(db_project)
        db.session.commit()

        flash("GitHub-Projekt wurde hinzugefügt.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Fehler beim Speichern: {str(e)}", "error")

    return redirect(url_for("admin.dashboard", active_tab="projects"))


@admin.route("/projects/github/<int:project_id>/edit", methods=["POST"])
@login_required
def edit_github_project(project_id):
    """GitHub-Projekt bearbeiten"""
    from flask_login import current_user
    from pathlib import Path
    from app.models import GitHubProject

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    data_dir = Path(__file__).parent.parent / "data"
    projects_file = data_dir / "github_projects.json"

    try:
        with open(projects_file, "r", encoding="utf-8") as f:
            projects = json.load(f)

        if 0 <= project_id < len(projects):
            # Projekt aktualisieren
            projects[project_id] = {
                "title": request.form.get("title"),
                "shortDescription": request.form.get("shortDescription"),
                "description": request.form.get("description"),
                "link": request.form.get("link"),
                "technologien": request.form.get("technologien", ""),
                "logo": request.form.get("logo", ""),
                "wip": request.form.get("wip") == "true",
            }

            # In JSON speichern
            with open(projects_file, "w", encoding="utf-8") as f:
                json.dump(projects, f, ensure_ascii=False, indent=4)

            # Datenbank synchronisieren: Alle löschen und neu laden
            GitHubProject.query.delete()
            db.session.commit()

            # Alle Projekte aus JSON neu in DB laden
            for proj_data in projects:
                db_project = GitHubProject(
                    title=proj_data.get("title", ""),
                    shortDescription=proj_data.get("shortDescription", ""),
                    types=proj_data.get("types", ""),
                    description=proj_data.get("description", ""),
                    link=proj_data.get("link", ""),
                    technologien=proj_data.get("technologien", ""),
                    logo=proj_data.get("logo", ""),
                    wip=proj_data.get("wip", False),
                )
                db.session.add(db_project)

            db.session.commit()
            flash("GitHub-Projekt wurde aktualisiert.", "success")
        else:
            flash("Projekt nicht gefunden.", "error")
    except Exception as e:
        db.session.rollback()
        flash(f"Fehler beim Aktualisieren: {str(e)}", "error")

    return redirect(url_for("admin.dashboard", active_tab="projects"))


@admin.route("/projects/github/<int:project_id>/delete", methods=["POST"])
@login_required
def delete_github_project(project_id):
    """GitHub-Projekt löschen"""
    from flask_login import current_user
    from pathlib import Path
    from app.models import GitHubProject

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    data_dir = Path(__file__).parent.parent / "data"
    projects_file = data_dir / "github_projects.json"

    try:
        with open(projects_file, "r", encoding="utf-8") as f:
            projects = json.load(f)

        if 0 <= project_id < len(projects):
            deleted_project = projects.pop(project_id)

            with open(projects_file, "w", encoding="utf-8") as f:
                json.dump(projects, f, ensure_ascii=False, indent=4)

            # Datenbank synchronisieren: Alle löschen und neu laden
            GitHubProject.query.delete()
            db.session.commit()

            # Alle Projekte aus JSON neu in DB laden
            for proj_data in projects:
                db_project = GitHubProject(
                    title=proj_data.get("title", ""),
                    shortDescription=proj_data.get("shortDescription", ""),
                    types=proj_data.get("types", ""),
                    description=proj_data.get("description", ""),
                    link=proj_data.get("link", ""),
                    technologien=proj_data.get("technologien", ""),
                    logo=proj_data.get("logo", ""),
                    wip=proj_data.get("wip", False),
                )
                db.session.add(db_project)

            db.session.commit()
            flash(
                f"Projekt '{deleted_project.get('title', '')}' wurde gelöscht.",
                "success",
            )
        else:
            flash("Projekt nicht gefunden.", "error")
    except Exception as e:
        db.session.rollback()
        flash(f"Fehler beim Löschen: {str(e)}", "error")

    return redirect(url_for("admin.dashboard", active_tab="projects"))


# ========== SKILLS ROUTES ==========


@admin.route("/skills/add", methods=["POST"])
@login_required
def add_skill():
    """Neuen Skill hinzufügen"""
    from flask_login import current_user
    from pathlib import Path

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    data_dir = Path(__file__).parent.parent / "data"
    skills_file = data_dir / "skills.json"

    try:
        # Bestehende Skills laden
        with open(skills_file, "r", encoding="utf-8") as f:
            skills = json.load(f)

        # Neuen Skill erstellen
        new_skill = {
            "name": request.form.get("name"),
            "level": request.form.get("level"),
            "icon": request.form.get("icon", ""),
            "info": request.form.get("info", ""),
            "description": request.form.get("description", ""),
            "link": request.form.get("link", ""),
            "category": request.form.get("category", "tools"),
        }

        # Skills in JSON speichern
        skills.append(new_skill)
        with open(skills_file, "w", encoding="utf-8") as f:
            json.dump(skills, f, ensure_ascii=False, indent=4)

        # Auch in Datenbank hinzufügen
        from app.models import Skill

        db_skill = Skill(
            name=request.form.get("name"),
            level=request.form.get("level"),
            icon=request.form.get("icon", ""),
            info=request.form.get("info", ""),
            description=request.form.get("description", ""),
            link=request.form.get("link", ""),
            category=request.form.get("category", "tools"),
        )
        db.session.add(db_skill)
        db.session.commit()

        flash(f"Skill '{new_skill['name']}' wurde hinzugefügt.", "success")
    except Exception as e:
        flash(f"Fehler beim Hinzufügen: {str(e)}", "error")
        db.session.rollback()

    return redirect(url_for("admin.dashboard", active_tab="skills"))


@admin.route("/skills/<int:skill_id>/edit", methods=["POST"])
@login_required
def edit_skill(skill_id):
    """Skill bearbeiten"""
    from flask_login import current_user
    from pathlib import Path
    from app.models import Skill

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    data_dir = Path(__file__).parent.parent / "data"
    skills_file = data_dir / "skills.json"

    try:
        with open(skills_file, "r", encoding="utf-8") as f:
            skills = json.load(f)

        if 0 <= skill_id < len(skills):
            # Skill in JSON aktualisieren
            skills[skill_id] = {
                "name": request.form.get("name"),
                "level": request.form.get("level"),
                "icon": request.form.get("icon", ""),
                "info": request.form.get("info", ""),
                "description": request.form.get("description", ""),
                "link": request.form.get("link", ""),
                "category": request.form.get("category", "tools"),
            }

            # In JSON speichern
            with open(skills_file, "w", encoding="utf-8") as f:
                json.dump(skills, f, ensure_ascii=False, indent=4)

            # Auch in Datenbank aktualisieren
            db_skills = Skill.query.all()
            if skill_id < len(db_skills):
                db_skill = db_skills[skill_id]
                db_skill.name = request.form.get("name")
                db_skill.level = request.form.get("level")
                db_skill.icon = request.form.get("icon", "")
                db_skill.info = request.form.get("info", "")
                db_skill.description = request.form.get("description", "")
                db_skill.link = request.form.get("link", "")
                db_skill.category = request.form.get("category", "tools")
                db.session.commit()

            flash("Skill wurde aktualisiert.", "success")
        else:
            flash("Skill nicht gefunden.", "error")
    except Exception as e:
        flash(f"Fehler beim Aktualisieren: {str(e)}", "error")
        db.session.rollback()

    return redirect(url_for("admin.dashboard", active_tab="skills"))


@admin.route("/skills/<int:skill_id>/delete", methods=["POST"])
@login_required
def delete_skill(skill_id):
    """Skill löschen"""
    from flask_login import current_user
    from pathlib import Path

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    data_dir = Path(__file__).parent.parent / "data"
    skills_file = data_dir / "skills.json"

    try:
        with open(skills_file, "r", encoding="utf-8") as f:
            skills = json.load(f)

        if 0 <= skill_id < len(skills):
            deleted_skill = skills.pop(skill_id)

            with open(skills_file, "w", encoding="utf-8") as f:
                json.dump(skills, f, ensure_ascii=False, indent=4)

            # Auch aus Datenbank löschen
            from app.models import Skill

            db_skills = Skill.query.all()
            if skill_id < len(db_skills):
                db.session.delete(db_skills[skill_id])
                db.session.commit()

            flash(f"Skill '{deleted_skill.get('name', '')}' wurde gelöscht.", "success")
        else:
            flash("Skill nicht gefunden.", "error")
    except Exception as e:
        flash(f"Fehler beim Löschen: {str(e)}", "error")
        db.session.rollback()

    return redirect(url_for("admin.dashboard", active_tab="skills"))


# ========== CERTIFICATIONS ROUTES ==========


@admin.route("/certifications/add", methods=["POST"])
@login_required
def add_certification():
    """Neues Zertifikat hinzufügen"""
    from flask_login import current_user

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    try:
        new_cert = Certification(
            name=request.form.get("name"),
            description=request.form.get("description"),
            date=request.form.get("date"),
            link=request.form.get("link", ""),
            image=request.form.get("image", ""),
        )
        db.session.add(new_cert)
        db.session.commit()

        flash(f"Zertifikat '{new_cert.name}' wurde hinzugefügt.", "success")
    except Exception as e:
        flash(f"Fehler beim Hinzufügen: {str(e)}", "error")
        db.session.rollback()

    return redirect(url_for("admin.dashboard", active_tab="certs"))


@admin.route("/certifications/<int:cert_id>/edit", methods=["POST"])
@login_required
def edit_certification(cert_id):
    """Zertifikat bearbeiten"""
    from flask_login import current_user

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    try:
        cert = Certification.query.get_or_404(cert_id)
        cert.name = request.form.get("name")
        cert.description = request.form.get("description")
        cert.date = request.form.get("date")
        cert.link = request.form.get("link", "")
        cert.image = request.form.get("image", "")
        db.session.commit()

        flash(f"Zertifikat '{cert.name}' wurde aktualisiert.", "success")
    except Exception as e:
        flash(f"Fehler beim Aktualisieren: {str(e)}", "error")
        db.session.rollback()

    return redirect(url_for("admin.dashboard", active_tab="certs"))


@admin.route("/certifications/<int:cert_id>/delete", methods=["POST", "GET"])
@login_required
def delete_certification(cert_id):
    """Zertifikat löschen"""
    from flask_login import current_user

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    try:
        cert = Certification.query.get_or_404(cert_id)
        cert_name = cert.name
        db.session.delete(cert)
        db.session.commit()

        flash(f"Zertifikat '{cert_name}' wurde gelöscht.", "success")
    except Exception as e:
        flash(f"Fehler beim Löschen: {str(e)}", "error")
        db.session.rollback()

    return redirect(url_for("admin.dashboard", active_tab="certs"))


# ========== IMPORT ROUTES ==========


@admin.route("/import/projects", methods=["POST"])
@login_required
def import_projects():
    """Portfolio-Projekte aus JSON-Datei importieren"""
    from flask_login import current_user
    from pathlib import Path
    from app.models import Project, Task

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    if "file" not in request.files:
        flash("Keine Datei ausgewählt.", "error")
        return redirect(url_for("admin.dashboard", active_tab="projects"))

    file = request.files["file"]
    if file.filename == "" or file.filename is None:
        flash("Keine Datei ausgewählt.", "error")
        return redirect(url_for("admin.dashboard", active_tab="projects"))

    if not file.filename.endswith(".json"):
        flash("Bitte eine JSON-Datei hochladen.", "error")
        return redirect(url_for("admin.dashboard", active_tab="projects"))

    try:
        # JSON aus Datei lesen
        content = file.read().decode("utf-8")
        data = json.loads(content)

        # Validieren, dass es eine Liste ist
        if not isinstance(data, list):
            # Prüfen ob es ein Export-Format ist (mit "data" key)
            if isinstance(data, dict) and "data" in data:
                data = data["data"]
            else:
                flash("Ungültiges Format. Erwartet wird ein JSON-Array.", "error")
                return redirect(url_for("admin.dashboard", active_tab="projects"))

        # JSON-Datei speichern
        data_dir = Path(__file__).parent.parent / "data"
        projects_file = data_dir / "projects.json"

        with open(projects_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        # Datenbank synchronisieren: Alle vorhandenen Projekte und Tasks löschen
        Task.query.delete()
        Project.query.delete()
        db.session.commit()

        # Neue Projekte aus JSON in Datenbank einfügen
        for project_data in data:
            # Aufgaben extrahieren und später als Tasks hinzufügen
            aufgaben = project_data.pop("aufgaben", [])

            # Projekt erstellen
            project = Project(
                title=project_data.get("title", ""),
                shortDescription=project_data.get("shortDescription", ""),
                rolle=project_data.get("rolle", ""),
                description=project_data.get("description", ""),
                technologien=project_data.get("technologien", ""),
                von=project_data.get("von", ""),
                bis=project_data.get("bis", ""),
                logo=project_data.get("logo", ""),
                link=project_data.get("link", ""),
                types=project_data.get("types", ""),
            )
            db.session.add(project)
            db.session.flush()  # Um die ID zu bekommen

            # Tasks hinzufügen
            for aufgabe in aufgaben:
                task = Task(description=aufgabe, project_id=project.id)
                db.session.add(task)

        db.session.commit()

        flash(
            f"✅ {len(data)} Portfolio-Projekte erfolgreich importiert und in Datenbank synchronisiert.",
            "success",
        )
    except json.JSONDecodeError as e:
        flash(f"Fehler beim Parsen der JSON-Datei: {str(e)}", "error")
    except Exception as e:
        db.session.rollback()
        flash(f"Fehler beim Importieren: {str(e)}", "error")

    return redirect(url_for("admin.dashboard", active_tab="projects"))


@admin.route("/import/github_projects", methods=["POST"])
@login_required
def import_github_projects():
    """GitHub-Projekte aus JSON-Datei importieren"""
    from flask_login import current_user
    from pathlib import Path
    from app.models import GitHubProject

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    if "file" not in request.files:
        flash("Keine Datei ausgewählt.", "error")
        return redirect(url_for("admin.dashboard", active_tab="projects"))

    file = request.files["file"]
    if file.filename == "" or file.filename is None:
        flash("Keine Datei ausgewählt.", "error")
        return redirect(url_for("admin.dashboard", active_tab="projects"))

    if not file.filename.endswith(".json"):
        flash("Bitte eine JSON-Datei hochladen.", "error")
        return redirect(url_for("admin.dashboard", active_tab="projects"))

    try:
        # JSON aus Datei lesen
        content = file.read().decode("utf-8")
        data = json.loads(content)

        # Validieren, dass es eine Liste ist
        if not isinstance(data, list):
            # Prüfen ob es ein Export-Format ist (mit "data" key)
            if isinstance(data, dict) and "data" in data:
                data = data["data"]
            else:
                flash("Ungültiges Format. Erwartet wird ein JSON-Array.", "error")
                return redirect(url_for("admin.dashboard", active_tab="projects"))

        # JSON-Datei speichern
        data_dir = Path(__file__).parent.parent / "data"
        projects_file = data_dir / "github_projects.json"

        with open(projects_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        # Datenbank synchronisieren: Alle vorhandenen GitHub-Projekte löschen
        GitHubProject.query.delete()
        db.session.commit()

        # Neue GitHub-Projekte aus JSON in Datenbank einfügen
        for project_data in data:
            github_project = GitHubProject(
                title=project_data.get("title", ""),
                shortDescription=project_data.get("shortDescription", ""),
                types=project_data.get("types", ""),
                description=project_data.get("description", ""),
                link=project_data.get("link", ""),
                technologien=project_data.get("technologien", ""),
                logo=project_data.get("logo", ""),
                wip=project_data.get("wip", False),
            )
            db.session.add(github_project)

        db.session.commit()

        flash(
            f"✅ {len(data)} GitHub-Projekte erfolgreich importiert und in Datenbank synchronisiert.",
            "success",
        )
    except json.JSONDecodeError as e:
        flash(f"Fehler beim Parsen der JSON-Datei: {str(e)}", "error")
    except Exception as e:
        db.session.rollback()
        flash(f"Fehler beim Importieren: {str(e)}", "error")

    return redirect(url_for("admin.dashboard", active_tab="projects"))


@admin.route("/import/skills", methods=["POST"])
@login_required
def import_skills():
    """Skills aus JSON-Datei importieren"""
    from flask_login import current_user
    from pathlib import Path

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    if "file" not in request.files:
        flash("Keine Datei ausgewählt.", "error")
        return redirect(url_for("admin.dashboard", active_tab="backup"))

    file = request.files["file"]
    if file.filename == "" or file.filename is None:
        flash("Keine Datei ausgewählt.", "error")
        return redirect(url_for("admin.dashboard", active_tab="backup"))

    if not file.filename.endswith(".json"):
        flash("Bitte eine JSON-Datei hochladen.", "error")
        return redirect(url_for("admin.dashboard", active_tab="backup"))

    try:
        content = file.read().decode("utf-8")
        data = json.loads(content)

        if not isinstance(data, list):
            if isinstance(data, dict) and "data" in data:
                data = data["data"]
            else:
                flash("Ungültiges Format. Erwartet wird ein JSON-Array.", "error")
                return redirect(url_for("admin.dashboard", active_tab="backup"))

        data_dir = Path(__file__).parent.parent / "data"
        skills_file = data_dir / "skills.json"

        with open(skills_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        flash(f"✅ {len(data)} Skills erfolgreich importiert.", "success")
    except json.JSONDecodeError as e:
        flash(f"Fehler beim Parsen der JSON-Datei: {str(e)}", "error")
    except Exception as e:
        flash(f"Fehler beim Importieren: {str(e)}", "error")

    return redirect(url_for("admin.dashboard", active_tab="backup"))


@admin.route("/import/certs", methods=["POST"])
@login_required
def import_certs():
    """Zertifikate aus JSON-Datei importieren"""
    from flask_login import current_user
    from pathlib import Path

    if not (hasattr(current_user, "get_id") and current_user.get_id() == "1"):
        flash("Zugriff verweigert.", "error")
        return redirect(url_for("main.index"))

    if "file" not in request.files:
        flash("Keine Datei ausgewählt.", "error")
        return redirect(url_for("admin.dashboard", active_tab="backup"))

    file = request.files["file"]
    if file.filename == "" or file.filename is None:
        flash("Keine Datei ausgewählt.", "error")
        return redirect(url_for("admin.dashboard", active_tab="backup"))

    if not file.filename.endswith(".json"):
        flash("Bitte eine JSON-Datei hochladen.", "error")
        return redirect(url_for("admin.dashboard", active_tab="backup"))

    try:
        content = file.read().decode("utf-8")
        data = json.loads(content)

        if not isinstance(data, list):
            if isinstance(data, dict) and "data" in data:
                data = data["data"]
            else:
                flash("Ungültiges Format. Erwartet wird ein JSON-Array.", "error")
                return redirect(url_for("admin.dashboard", active_tab="backup"))

        data_dir = Path(__file__).parent.parent / "data"
        certs_file = data_dir / "certs.json"

        with open(certs_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        flash(f"✅ {len(data)} Zertifikate erfolgreich importiert.", "success")
    except json.JSONDecodeError as e:
        flash(f"Fehler beim Parsen der JSON-Datei: {str(e)}", "error")
    except Exception as e:
        flash(f"Fehler beim Importieren: {str(e)}", "error")

    return redirect(url_for("admin.dashboard", active_tab="backup"))


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
            "name": getattr(about, "name", None),
            "title": getattr(about, "title", None),
            "description": getattr(about, "description", None),
            "image": getattr(about, "image", None),
        }

    # Timeline
    timeline_items = TimelineItem.query.order_by(
        getattr(TimelineItem, "position")
    ).all()
    for item in timeline_items:
        data["timeline"].append(
            {
                "id": getattr(item, "id", None),
                "title": getattr(item, "title", None),
                "organization": getattr(item, "organization", None),
                "date": getattr(item, "date", None),
                "description": getattr(item, "description", None),
                "icon": getattr(item, "icon", None),
                "position": getattr(item, "position", None),
                "is_active": getattr(item, "is_active", None),
            }
        )

    # Contact
    contact = Contact.query.first()
    if contact:
        data["contact"] = {
            "vorname": getattr(contact, "vorname", None),
            "nachname": getattr(contact, "nachname", None),
            "email": getattr(contact, "email", None),
            "linkedin": getattr(contact, "linkedin", None),
            "github": getattr(contact, "github", None),
            "profile_image": getattr(contact, "profile_image", None),
        }

    # Access Requests
    requests = AccessRequest.query.all()
    for req in requests:
        data["access_requests"].append(
            {
                "id": getattr(req, "id", None),
                "email": getattr(req, "email", None),
                "created_at": (
                    req.created_at.isoformat()
                    if getattr(req, "created_at", None)
                    else None
                ),
                "token_expires": (
                    req.token_expires.isoformat()
                    if getattr(req, "token_expires", None)
                    else None
                ),
                "is_active": getattr(req, "is_active", None),
                "status": getattr(req, "status", None),
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
                    file_content = f.read().strip()
                    if file_content:
                        data[key] = json.loads(file_content)
                    else:
                        data[key] = []
            except Exception as e:
                data[key] = {"error": str(e)}
        else:
            data[key] = []

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
                "greeting": about.greeting,
                "shortDescription": about.short_description,
                "bio": about.bio,
                "role": about.role,
                "dynamics365Since": about.dynamics365_since,
            }
        else:
            data["data"] = {}

    elif data_type == "timeline":
        timeline_items = TimelineItem.query.order_by(
            getattr(TimelineItem, "position")
        ).all()
        data["data"] = []
        for item in timeline_items:
            data["data"].append(
                {
                    "id": item.id,
                    "title": item.title,
                    "organization": getattr(item, "organization", None),
                    "date": getattr(item, "date", None),
                    "description": item.description,
                    "icon": getattr(item, "icon", None),
                    "position": item.position,
                    "is_active": item.is_active,
                }
            )
        # Falls keine Timeline-Items vorhanden, bleibt data["data"] leeres Array

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
        else:
            data["data"] = {}

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
                    "is_used": getattr(req, "is_used", None),
                }
            )
        # Falls keine Requests vorhanden, bleibt data["data"] leeres Array

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
