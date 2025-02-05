# app/routes.py
from flask import Blueprint, render_template
from datetime import datetime

from app.models import Contact
from app.data import load_projects, parse_date


main = Blueprint("main", __name__)


# Beispielroute
@main.route("/")
def index():
    my_contact = Contact(
        vorname="Sebastian",
        nachname="Meine",
        role="Microsoft Dynamics 365 Professional",
        email="sebastian.meine@meinedevpath.de",
        linkedin="https://www.linkedin.com/in/sebastianmeine1985/",
        github="https://github.com/EsstBananeImEi",
    )

    project_data = load_projects("projects.json")
    skills = load_projects("skills.json")
    projects = project_data.get("projects", [])
    github_projects = project_data.get("gitprojects", [])

    projects = sorted(projects, key=lambda p: parse_date(p.get("bis")), reverse=True)
    skills = sorted(skills, key=lambda p: p.get("name"))

    about = {
        "name": f"{my_contact.vorname} {my_contact.nachname}",
        "role": my_contact.role,
        "greeting": f"Hallo, ich bin {my_contact.vorname}!",
        "bio": """„Als erfahrener Entwickler und Consultant mit einem Fokus auf Microsoft Dynamics 365 
spezialisiere ich mich auf die maßgeschneiderte Konzeption und Implementierung komplexer CRM-Lösungen. 
Ich helfe Unternehmen dabei, ihre Geschäftsprozesse zu automatisieren und ihre Systemarchitekturen nachhaltig zu optimieren. 
Zusätzlich bringe ich fundierte Expertise in der Entwicklung von modernen Web- und Softwarelösungen mit Python, 
JavaScript und C# ein. Mit einem klaren Blick auf Effizienzsteigerung und zukunftsfähige Technologien strebe ich stets danach, 
innovative Lösungen zu entwickeln, die Unternehmen dabei unterstützen, 
ihre digitalen Transformationsziele zu erreichen und langfristig wettbewerbsfähig zu bleiben.“
""",
        "profile_image": "./static/images/CRM_Meine_1.jpg",
    }

    contact = my_contact.__dict__

    return render_template(
        "index.html",
        projects=projects,
        github_projects=github_projects,
        about=about,
        contact=contact,
        skills=skills,
        now=datetime.now(),
    )
