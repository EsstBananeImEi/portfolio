# app/routes.py
from flask import Blueprint, render_template
from datetime import datetime

from app.models import Certification, Contact, About, Project, GitHubProject, Skill
from app.data import parse_date, load_data, load_data_list


main = Blueprint("main", __name__)


@main.route("/")
def index():

    projects = load_data_list(Project, "projects.json")
    github_projects = load_data_list(GitHubProject, "github_projects.json")
    skills = load_data_list(Skill, "skills.json")
    about = load_data(About, "about.json")
    contact = load_data(Contact, "contact.json")
    certifications = load_data_list(Certification, "certs.json")

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
