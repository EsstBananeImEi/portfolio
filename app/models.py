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
    bio = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(255), nullable=True)


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

    def __init__(self, **kwargs):
        tasks_data = kwargs.pop("aufgaben", None)
        super().__init__(**kwargs)
        if tasks_data:
            self.tasks = [Task(description=desc, project_id=id) for desc in tasks_data]


class GitHubProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    shortDescription = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(255), nullable=False)
    technologien = db.Column(db.String(255), nullable=False)
    logo = db.Column(db.String(255), nullable=False)
    wip = db.Column(db.Boolean, nullable=False)


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    level = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(255), nullable=False)
    info = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255), nullable=False)


class Certification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(255), nullable=False)
