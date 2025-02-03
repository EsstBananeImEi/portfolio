from flask import Flask, render_template, url_for
from datetime import datetime

app = Flask(__name__)


# Kontaktobjekt
class Contact:
    def __init__(self, vorname, nachname, role, email, linkedin, github):
        self.vorname = vorname
        self.nachname = nachname
        self.role = role
        self.email = email
        self.linkedin = linkedin
        self.github = github


# Kontakt-Objekt erstellen
my_contact = Contact(
    vorname="Sebastiaaaan",
    nachname="Meine",
    role="Microsoft Dynamics 365 Professional",
    email="sebastian.meine@gmx.net",
    linkedin="https://www.linkedin.com/in/sebastianmeine1985/",
    github="https://github.com/EsstBananeImEi",
)


@app.route("/")
def index():
    # Hauptprojekte
    projects = [
        {
            "title": "CRM-Entwicklung",
            "description": "Entwicklung und Erweiterung eines Dynamics 365 CRM-Systems mit Fokus auf Benutzerfreundlichkeit und Automatisierung.",
            "link": "https://vdivde-it.de/en",
            "technologies": "C#, JavaScript, React, Dynamics 365 CE, Power Automate",
            "logo": "./static/images/vdivde.png",
        },
        {
            "title": "Automatisierung von Geschäftsprozessen",
            "description": "Teil- bis Vollautomatisierung von Geschäftsprozessen im Bereich betriebliche Altersvorsorge mit Dynamics 365.",
            "link": "https://www.ergo.com/de",
            "technologies": "C#, JavaScript, Dynamics 365 CE",
            "logo": "./static/images/ergo.png",
        },
        {
            "title": "Energie-Managementsystem",
            "description": "Migration von SmartCRM zu Dynamics 365, Analyse und Kostenabschätzung für die Integration interner Lösungen.",
            "link": "https://hochhuth.de/software/",
            "technologies": "C#, JavaScript, SSIS, Dynamics 365 CE",
            "logo": "./static/images/hochhuth.png",
        },
        {
            "title": "Marktreife Einführung des HMI-Prototyps",
            "description": "Führt einen HMI-Prototyp mittels Microservices in den Markt ein.",
            "link": "https://www.schottel.de/home",
            "technologies": "Python, Jenkins, Git, MQTT, ZeroMQ, Microservices, SQLite, Django",
            "logo": "./static/images/schottel.png",
        },
        {
            "title": "Prototyp-Entwicklung zur Schiffsdaten-Analyse",
            "description": "Entwicklung eines HMI zur Erfassung und Analyse schiffsbezogener Daten.",
            "link": "https://www.schottel.de/home",
            "technologies": "Python, MQTT, ZeroMQ, Django, SQLite, Docker",
            "logo": "./static/images/schottel.png",
        },
        {
            "title": "CRM-Weiterentwicklung",
            "description": "Optimierung von UI, DSGVO-Anforderungen und Asset Management im CRM.",
            "link": "https://www.lufthansa-industry-solutions.com/",
            "technologies": "JavaScript, C#, Node.js, Power Automate",
            "logo": "./static/images/lufthansa.png",
        },
        {
            "title": "Datenverarbeitungssystem",
            "description": "Agile Integration von Dynamics 365 CE in vier Geschäftsbereiche.",
            "link": "https://www.commerzreal.com/",
            "technologies": "JavaScript, C#, PCF-Control, Node.js",
            "logo": "./static/images/Commerz_Real_logo.svg",
        },
        {
            "title": "Modernisierung interner Python Software",
            "description": "Analyse, Optimierung und Weiterentwicklung interner Prozesse mit Git, Jenkins und FastAPI.",
            "link": "https://www.meta-trennwandanlagen.de/",
            "technologies": "Python, Jenkins, Git, Prometheus, Grafana, InformixDB, FastAPI, Flask",
            "logo": "./static/images/meta.png",
        },
        {
            "title": "Warehouse Management",
            "description": "Implementierung eines internen Webportals zur Lagerbestandsverwaltung.",
            "link": None,
            "technologies": "React, TypeScript, SQLite",
            "logo": None,
        },
        {
            "title": "Internes Logistik-Webportal",
            "description": "Entwicklung eines Webportals zur Lagerverwaltung und Bestandsüberwachung.",
            "link": None,
            "technologies": "React, TypeScript, SQLite, Flask",
            "logo": None,
        },
    ]

    # GitHub-Projekte (Open-Source-Projekte)
    github_projects = [
        {
            "title": "Python-Kurs",
            "description": "Kursmaterialien und Beispielcode für meinen Python-Kurs auf Udemy.",
            "link": "https://github.com/EsstBananeImEi/python-kurs",
            "technologies": "Python",
            "logo": f"./static/images/kurs-bild.jpg",
        },
        {
            "title": "Flask-Portfolio",
            "description": "Ein schlankes Portfolio-Template für Flask.",
            "link": "https://github.com/EsstBananeImEi/portfolio",
            "technologies": "Python, Flask",
            "logo": "./static/images/LOGONEU.png",
        },
        {
            "title": "Prepper App",
            "description": "Eine einfache Web-App zur Vorratsplanung. Ideal für Prepper und Krisenvorsorger.",
            "link": "https://github.com/EsstBananeImEi/prepper-app",
            "technologies": "React, TypeScript",
            "logo": "./static/images/prepper-app.svg",
        },
    ]

    about = {
        "name": f"{my_contact.vorname} {my_contact.nachname}",
        "role": my_contact.role,
        "greeting": f"Hallo, ich bin {my_contact.vorname}!",
        "bio": """„Ich bin ein erfahrener Entwickler und Consultant mit Schwerpunkt auf Microsoft Dynamics 365.
Ich konzipiere und implementiere individuelle CRM-Lösungen, automatisiere Geschäftsprozesse 
und optimiere Systemarchitekturen. Neben meiner Arbeit im Dynamics-365-Umfeld entwickle ich 
moderne Web- und Softwarelösungen mit Python, JavaScript und C#. Mein Ziel ist es, 
Unternehmen durch innovative Technologien effizienter und zukunftssicher zu machen.“""",
        "profile_image": "./static/images/CRM_Meine_1.jpg",
    }

    contact = my_contact.__dict__

    skills = [
        {"name": "Python", "level": "Expert", "icon": "devicon-python-plain"},
        {"name": "Flask", "level": "Intermediate", "icon": "devicon-flask-original"},
        {"name": "HTML5", "level": "Advanced", "icon": "devicon-html5-plain"},
        {"name": "JavaScript", "level": "Advanced", "icon": "devicon-javascript-plain"},
        {"name": "React", "level": "Advanced", "icon": "devicon-react-original"},
        {"name": "Node.js", "level": "Intermediate", "icon": "devicon-nodejs-plain"},
        {"name": "C#", "level": "Advanced", "icon": "devicon-csharp-plain"},
        {"name": "Docker", "level": "Intermediate", "icon": "devicon-docker-plain"},
        {"name": "Git", "level": "Advanced", "icon": "devicon-git-plain"},
        {"name": "Linux", "level": "Advanced", "icon": "devicon-linux-plain"},
        {"name": "MySQL", "level": "Intermediate", "icon": "devicon-mysql-plain"},
        {
            "name": "PostgreSQL",
            "level": "Intermediate",
            "icon": "devicon-postgresql-plain",
        },
        {"name": "SQLite", "level": "Advanced", "icon": "devicon-sqlite-plain"},
        {
            "name": "Dynamics 365",
            "level": "Expert",
            "icon": "static/images/dynamics.png",
        },
    ]

    return render_template(
        "index.html",
        projects=projects,
        github_projects=github_projects,
        about=about,
        contact=contact,
        skills=skills,
        now=datetime.now(),
    )
