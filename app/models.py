from app import db
from flask_login import UserMixin


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vorname = db.Column(db.String(255), nullable=False)
    nachname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    linkedin = db.Column(db.String(255), nullable=False)
    github = db.Column(db.String(255), nullable=False)
    profile_image = db.Column(db.String(255), nullable=False)

    def get_full_name(self):
        return f"{self.vorname} {self.nachname}"


class About(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    greeting = db.Column(db.String(255), nullable=False)
    short_description = db.Column(db.Text, nullable=True)
    bio = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(255), nullable=True)
    dynamics365_since = db.Column(db.Integer, nullable=True)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)

    def __init__(self, description, project_id) -> None:
        self.description = description
        self.project_id = project_id
        super().__init__()


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    shortDescription = db.Column(db.String(255), nullable=False)
    rolle = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tasks = db.relationship("Task", backref="project", lazy=True)
    technologien = db.Column(db.String(255), nullable=False)
    von = db.Column(db.String(255), nullable=False)
    bis = db.Column(db.String(255), nullable=False)
    logo = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255), nullable=True)
    types = db.Column(db.String(255), nullable=True)  # z.B. "dynamics,software"

    def __init__(self, **kwargs):
        tasks_data = kwargs.pop("aufgaben", None)
        super().__init__(**kwargs)
        if tasks_data:
            self.tasks = [Task(description=desc, project_id=id) for desc in tasks_data]


class GitHubProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    shortDescription = db.Column(db.String(255), nullable=False)
    types = db.Column(db.String(255), nullable=True)  # z.B. "software,web"
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(255), nullable=False)
    technologien = db.Column(db.String(255), nullable=False)
    logo = db.Column(db.String(255), nullable=False)
    wip = db.Column(db.Boolean, nullable=False)

    def __init__(
        self,
        title,
        shortDescription,
        description,
        link,
        technologien,
        logo,
        wip=False,
        types=None,
    ):
        self.title = title
        self.shortDescription = shortDescription
        self.description = description
        self.link = link
        self.technologien = technologien
        self.logo = logo
        self.wip = wip
        self.types = types


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    level = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(255), nullable=False)
    info = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False, default="tools")

    def __init__(self, name, level, icon, info, description, link, category="tools"):
        self.name = name
        self.level = level
        self.icon = icon
        self.info = info
        self.description = description
        self.link = link
        self.category = category


class Certification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(255), nullable=False)

    def __init__(self, name, description, date, image, link=None):
        self.name = name
        self.description = description
        self.date = date
        self.link = link
        self.image = image


class TimelineItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer, nullable=False, default=0)  # Sortierung
    period_start = db.Column(db.String(50), nullable=False)  # z.B. "2020"
    period_end = db.Column(db.String(50), nullable=False)  # z.B. "Heute"
    title = db.Column(db.String(255), nullable=False)  # z.B. "Senior Consultant"
    company = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    badge = db.Column(db.String(100), nullable=True)  # z.B. "Aktuell"
    badge_color = db.Column(
        db.String(50), nullable=True, default="success"
    )  # primary, accent, success, warning
    icon_type = db.Column(
        db.String(50), nullable=True, default="microsoft"
    )  # microsoft, code, briefcase
    tags = db.Column(
        db.String(500), nullable=True
    )  # Komma-getrennt: "Dynamics 365,C#,Power Platform"
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(
        self,
        position,
        period_start,
        period_end,
        title,
        company,
        description,
        badge=None,
        badge_color=None,
        icon_type=None,
        tags=None,
        is_active=True,
    ):
        self.position = position
        self.period_start = period_start
        self.period_end = period_end
        self.title = title
        self.company = company
        self.description = description
        self.badge = badge
        self.badge_color = badge_color
        self.icon_type = icon_type
        self.tags = tags
        self.is_active = is_active


class AccessRequest(db.Model, UserMixin):
    """Anfragen für Zugriff auf die Portfolio-Projekte - mit Login-Funktionalität"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    status = db.Column(
        db.String(50), nullable=False, default="pending"
    )  # pending, approved, rejected
    token = db.Column(db.String(64), nullable=True, unique=True)
    token_expires = db.Column(db.DateTime, nullable=True)

    # Login-Felder
    password_hash = db.Column(db.String(256), nullable=True)  # Verschlüsseltes Passwort
    is_active = db.Column(db.Boolean, nullable=False, default=False)  # Account aktiv?
    last_login = db.Column(db.DateTime, nullable=True)  # Letzter Login

    def __init__(self, name, email, message=None, status="pending"):
        self.name = name
        self.email = email
        self.message = message
        self.status = status
        super().__init__()

    def is_access_valid(self):
        """Prüft ob der Zugriff noch gültig ist (für Projektzugriff)"""
        from datetime import datetime

        # Status muss approved sein
        if self.status != "approved":
            return False
        # Wenn Token-Ablaufdatum gesetzt ist, muss es in der Zukunft liegen
        if self.token_expires and self.token_expires < datetime.now():
            return False
        return True

    def is_token_expired(self):
        """Prüft ob der Token abgelaufen ist"""
        from datetime import datetime

        if not self.token_expires:
            return False
        return self.token_expires < datetime.now()

    def get_id(self):
        """Flask-Login: User-ID zurückgeben (mit Präfix um von Admin zu unterscheiden)"""
        return f"portfolio_{self.id}"
