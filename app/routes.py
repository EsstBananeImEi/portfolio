# app/routes.py
from flask import Blueprint, render_template
from datetime import datetime

from app.models import Certification, Contact, About, Project, GitHubProject, Skill
from app.data import parse_date, load_data, load_data_list


main = Blueprint("main", __name__)


@main.route("/")
def index():

    projects = Project.query.all()
    github_projects = GitHubProject.query.all()
    skills = Skill.query.all()
    about = About.query.first()
    contact = Contact.query.first()
    certifications = Certification.query.all()

    certifications = sorted(
        certifications, key=lambda cert: parse_date(cert.date), reverse=True
    )

    projects = sorted(
        projects, key=lambda project: parse_date(project.bis), reverse=True
    )
    skills = sorted(skills, key=lambda skill: skill.name)

    return render_template(
        "index.html",
        projects=projects,
        github_projects=github_projects,
        about=about,
        contact=contact,
        skills=skills,
        certifications=certifications,
        now=datetime.now(),
    )
