# app/routes.py
from flask import Blueprint, render_template
from datetime import datetime

from app.models import Contact
from app.templates.data import parse_date


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

    projects = [
        {
            "title": "CRM-Entwicklung bei VDI/VDE Innovation + Technik GmbH",
            "shortDescription": "Entwicklung und Erweiterung eines Dynamics 365 CRM-Systems...",
            "rolle": "Dynamics 365 CE Developer / Consultant",
            "description": (
                "Die VDI/VDE Innovation + Technik GmbH ist ein Projektträger sowie "
                "Dienstleistungs- und Beratungsunternehmen für verschiedene Bundes- und "
                "Landesministerien, die Europäische Kommission sowie die Finanzwirtschaft und "
                "Industrie – vor allem für kleine und mittlere Unternehmen. Im Fokus stehen "
                "gesellschaftliche und technische Herausforderungen wie Digitalisierung, "
                "demografischer Wandel, Mensch-Technik-Interaktion, Elektromobilität, Elektronik, "
                "Gesundheit, Bildung und Fragen der Innovationspolitik."
            ),
            "aufgaben": [
                "Neu- und Weiterentwicklung von Anforderungen",
                "Analyse, Konzeption und Implementierung von komplexen Lösungen im Zuge der Weiterentwicklung von neuen und bestehenden Applikationen",
            ],
            "technologien": "Javascript, C#, React",
            "von": "01/2024",
            "bis": "Aktuell",
            "logo": "./static/images/vdivde.png",
            "link": "https://vdivde-it.de/en",
        },
        {
            "title": "Automatisierung von Geschäftsprozessen bei Longial",
            "shortDescription": "Teil- bis Vollautomatisierung von Geschäftsprozessen im Unternehmen...",
            "rolle": "Dynamics 365 CE Developer / Consultant",
            "description": (
                "Longial bietet als eigenständiger und neutraler Dienstleister Lösungen zu allen Fragen der "
                "betrieblichen Altersversorgung aus einer Hand. Im Fokus des Projekts steht die teilweise bis "
                "vollständige Automatisierung von Geschäftsprozessen im Unternehmen."
            ),
            "aufgaben": [
                "Neu- und Weiterentwicklung von Anforderungen",
                "Analyse, Konzeption und Implementierung von komplexen Lösungen im Zuge der Weiterentwicklung von neuen und bestehenden Applikationen",
                "Analyse, Konzeption und Implementierung neuer sowie bestehender Geschäftsprozesse",
            ],
            "technologien": "Javascript, C#",
            "von": "09/2023",
            "bis": "12/2023",
            "logo": "./static/images/ergo.png",
            "link": "https://www.ergo.com/de/unternehmen/ueber-ergo/technologie-und-service-provider/itergo-informationstechnologie",
        },
        {
            "title": "Energie-Managementsystem bei HOCHHUTH GmbH",
            "shortDescription": "Migration von SmartCRM und Integration von Energiemanagement-Lösungen...",
            "rolle": "Dynamics 365 CE Developer / Consultant",
            "description": (
                "HOCHHUTH bietet umfassende Energiemanagement-Lösungen an, darunter das ENERGY IN INDUSTRY® System, das Unternehmen hilft, ihre Energiekosten zu senken. Basierend auf dem M-Bus ermöglicht es die Online-Zählerfernauslesung und wurde bereits in über 500 Unternehmen erfolgreich implementiert. Ihr Firmensitz beherbergt Europas größtes M-Bus System und dient als Plattform für zukünftige Technologieentwicklungen im Energiemanagement. Zusätzlich beraten sie Unternehmen bei der Auswahl von Zähleinrichtungen und der Optimierung von Energieerzeugungsanlagen."
            ),
            "aufgaben": [
                "Unterstützung bei der Migration von SmartCRM auf Dynamics 365",
                "Analyse, Konzeption und Implementierung neuer Funktionalitäten",
                "Analyse und Kostenschätzung für die Integration von unternehmenseigenen Softwarelösungen in Dynamics 365.",
            ],
            "technologien": "Javascript, C#, SSIS",
            "von": "08/2023",
            "bis": "11/2023",
            "logo": "./static/images/hochhuth.png",
            "link": "https://hochhuth.de/software/",
        },
        {
            "title": "Digitalisierung bei Lufthansa Industry Solutions",
            "shortDescription": "Unterstützung bei der Digitalisierung und Automatisierung von Geschäftsprozessen...",
            "rolle": "Dynamics 365 CE Developer",
            "description": (
                "Lufthansa Industry Solutions unterstützt Unternehmen bei der dafür notwendigen Digitalisierung und Automatisierung ihrer Geschäftsprozesse – vom Mittelständler bis zum DAX-Konzern. Dabei legen sie ihren Fokus nicht nur auf die dafür notwendige IT, sondern auf das Geschäft ihrer Kunden mit seinen internen und externen Herausforderungen. Denn die digitale Transformation umfasst die gesamte Unternehmensstruktur und -kultur und reicht über die Unternehmensgrenzen hinaus bis hin zur Zusammenarbeit mit Partnern, Kunden und Lieferanten."
            ),
            "aufgaben": [
                "Analyse, Konzeption und Implementierung von komplexen Lösungen im Zuge der Weiterentwicklung von neuen und bestehenden Applikationen",
                "Lösungen für UI-Erweiterungen, DSGVO und Asset-Management Funktionen",
                "Verwaltung und Deployment der entwickelten Anpassungen",
            ],
            "technologien": "Javascript, C#, nodeJs, Power Automate",
            "von": "08/2022",
            "bis": "11/2022",
            "logo": "./static/images/lufthansa.png",
            "link": "https://www.lufthansa-industry-solutions.com/de-en/",
        },
        {
            "title": "Asset Management bei Commerz Real",
            "shortDescription": "Anpassung und Integration des CRM-Systems für Asset Management...",
            "rolle": "Dynamics 365 CE Developer",
            "description": (
                "Die Commerz Real ist ein Asset Manager mit umfassendem Know-how im Assetmanagement und einer breiten Strukturierungsexpertise zur bündeln von Investmentprodukten für private und institutionelle Anleger, individuellen Finanzierungsstrukturierungen für gewerbliche Projekte und alternativen Finanzierungslösungen für Firmenkunden"
                "Der Fokus des Projekts liegt darin, das CRM-System den digitalen Anforderungen anzupassen und zu integrieren. Die Durchführung erfolgt in agiler Methodik, unter Einsatz von User Stories, Epics und Features."
            ),
            "aufgaben": [
                "Analyse, Konzeption und Implementierung von komplexen Lösungen im Zuge der Weiterentwicklung von bestehenden Applikationen für vier Unternehmensbereiche",
                "Lösungen für UI Erweiterungen, DSGVO und Asset-Management Funktionen",
                "Verwaltung und Deployment der entwickelten Anpassungen",
            ],
            "technologien": "Javascript, C#, PCF-Control, nodeJs",
            "von": "05/2022",
            "bis": "09/2022",
            "logo": "./static/images/Commerz_Real_logo.svg",
            "link": "https://www.commerzreal.com/",
        },
        {
            "title": "Einführung einer Mandantenfähigkeit im CRM-System",
            "shortDescription": "Erstellung und Implementierung einer Mandantenfähigkeit in Dynamics 365 CE...",
            "rolle": "Dynamics 365 CE Developer / Consultant",
            "description": (
                "Die VDI/VDE Innovation + Technik GmbH ist ein Projektträger sowie Dienstleistungs- und Beratungsunternehmen für verschiedene Bundes- und Landesministerien, die Europäische Kommission sowie die Finanzwirtschaft und die Industrie, dort vor allem für Kleine und mittlere Unternehmen. Im Fokus stehen gesellschaftliche und technische Herausforderungen wie Digitalisierung, demografischer Wandel, Mensch-Technik-Interaktion, Elektromobilität, Elektronik, Gesundheit, Bildung und Fragen der Innovationspolitik."
                "Der Fokus des Projekts liegt darin, das CRM-System auf ein akzeptables Niveau zu entwickeln, die Benutzerfreundlichkeit zu verbessern und funktionale Aktivitäten zu implementieren. Die Durchführung umfasste die Einführung in die agile Methodik, den Einsatz von User Stories, Epics und Features, die Erstellung und Durchführung von Workshops, Trainings, Show und Tells sowie UAT."
            ),
            "aufgaben": [
                "Neu- und Weiterentwicklung von Anforderungen",
                "Analyse, Konzeption und Implementierung einer Softwarelösung zur Automatisierung der Benutzerzuordnung in Dynamics 365",
                "Verwaltung und Deployment der entwickelten Anpassungen",
                "Entwicklung einer effizienteren Deployment-Strategie",
                "Umstrukturierung des Repositorys zur besseren Auffindbarkeit relevanter Inhalte",
                "Einführung von Unittests in das System zur Sicherzustellung der Code-Qualität und Funktionalität.",
            ],
            "technologien": "Javascript, C#, React",
            "von": "01/2022",
            "bis": "08/2023",
            "logo": "./static/images/vdivde.png",
            "link": "https://vdivde-it.de/en",
        },
        {
            "title": "Internes Logistik-Webportal",
            "shortDescription": "Entwicklung eines internen Webportals zur Aufnahme von Lagerbeständen...",
            "rolle": "Projektleiter / Senior Developer / Analyst",
            "description": (
                "Für ein Kleinunternehmen im Logistiksektor wurde ein Webportal entwickelt, das die Erfassung und Verwaltung "
                "von Lagerbeständen ermöglicht. Hierbei wurden sowohl die Infrastruktur geplant als auch die Umsetzung der Lösung "
                "koordiniert."
            ),
            "aufgaben": [
                "Analyse der Anforderungen und Planung der Infrastruktur",
                "Umsetzung des Webportals und Definition von Datenstrukturen",
                "Erstellung der Programmdokumentation",
                "Durchführung statischer Codeanalysen und automatisierter Tests",
                "Einführung von Continous Delivery Pipelines",
            ],
            "technologien": "React, Typescript, SQLite",
            "von": "07/2021",
            "bis": "09/2021",
            "logo": "./static/images/logistik.svg",
            "link": None,
        },
        {
            "title": "Modernisierung interner Software bei Meta Trennwandanlagen",
            "shortDescription": "Modernisierung und Wartung der bestehenden Softwarelandschaft, Einführung von CI/CD-Pipelines...",
            "rolle": "Projektleiter / Senior Developer / Analyst",
            "description": (
                "Sie sind Experten auf zahlreichen Anwendungsbereichen und bieten passende Produkte für jede Branche. Neben WC-Trennwänden für Gastronomie und Hotels sowie Büros und öffentliche Einrichtungen haben sie sich auf weitere Einsatzgebiete spezialisiert. Dazu gehören Schulen, Kindergärten und Kindertagesstätten, Sportanlagen und Schwimmbäder. In diesen Einrichtungen benötigen ihre Kunden Duschtrennwände, Schränke und Bänke mit Hakenleisten. Daher stattet das Unternehmen sie mit hochwertigen Produkten für Sanitär- sowie Umkleideräume und maßgeschneiderten Lösungen aus. Für Meta Trennwandanlagen wurde die bestehende Softwarelandschaft modernisiert. Neben der Wartung und "
                "Optimierung interner Prozesse wurden individuelle Anpassungen implementiert – unterstützt durch den Einsatz von "
                "Tools wie Git und Jenkins."
            ),
            "aufgaben": [
                "Modernisierung und Wartung der bestehenden Softwarelandschaft",
                "Implementierung individueller Anpassungen",
                "Analyse und Optimierung interner Prozesse",
                "Einführung von Continous Delivery Pipelines",
            ],
            "technologien": "Python, Jenkins, Git, Prometheus, Grafana, InformixDB, FastApi, Flask",
            "von": "02/2021",
            "bis": "07/2021",
            "logo": "./static/images/meta.png",
            "link": "https://www.meta.de/de/",
        },
        {
            "title": "Marktreife Einführung des HMI-Prototyps",
            "shortDescription": "Überführung des Datensammler-Prototyps in den Release und Schulung der Außendienstmitarbeiter...",
            "rolle": "Senior Developer / Analyst / Tester / Software Architekt",
            "description": (
                "Im Schiffsbausektor wurde ein Datensammler-Prototyp weiterentwickelt und in den offiziellen Release überführt. "
                "Neben der Weiterentwicklung der Programmelemente erfolgte auch eine umfassende Schulung der Außendienstmitarbeiter "
                "sowie eine abschließende Feedbackanalyse."
            ),
            "aufgaben": [
                "Überführung des Datensammler-Prototyps in den Release",
                "Schulung der Außendienstmitarbeiter",
                "Analyse und Behebung finaler Probleme",
            ],
            "technologien": "Python, Jenkins, Git, MQTT, ZeroMQ, Microservices, SQLite, Gherkin, Cucumber, Jasmine, Confluence, Jira, Django",
            "von": "10/2020",
            "bis": "01/2021",
            "logo": "./static/images/schottel.png",
            "link": "https://www.schottel.de/home",
        },
        {
            "title": "Prototyp-Entwicklung zur Schiffsdaten-Analyse",
            "shortDescription": "Entwicklung eines Prototyps zur Sammlung und Analyse schiffbezogener Daten...",
            "rolle": "Senior Developer / Analyst / Tester / Software Architekt",
            "description": (
                "In einem weiteren Projekt im Schiffsbau wurde ein Prototyp entwickelt, der die Erfassung und Analyse "
                "schiffbezogener Daten ermöglicht. Ergänzt wurde dies durch ein Kundenportal, in dem die Daten visualisiert werden."
            ),
            "aufgaben": [
                "Entwicklung eines Prototyps zur Sammlung schiffbezogener Daten",
                "Definition von Datenstrukturen und Kommunikationswegen",
                "Beratung und Umsetzung von Automatisierungslösungen",
                "Testen der Software unter Anwenderbedingungen",
                "Erstellung und Pflege der Programmdokumentation",
            ],
            "technologien": "Python, Jenkins, Git, MQTT, ZeroMQ, Microservices, SQLite, Gherkin, Cucumber, Jasmine, Confluence, Jira, Django",
            "von": "05/2019",
            "bis": "10/2020",
            "logo": "./static/images/schottel.png",
            "link": "https://www.schottel.de/home",
        },
        {
            "title": "Proof of Concept Schiffsdaten",
            "shortDescription": "Erstellung eines Proof of Concept zur Validierung kritischer Anforderungen im Schiffsbau...",
            "rolle": "Senior Developer / Analyst / Tester / PO",
            "description": (
                "Im Rahmen eines Projekts im Schiffsbausektor wurde ein Proof of Concept entwickelt, um kritische Anforderungen zu "
                "validieren. Dazu gehörten Marktforschung, Bedarfsanalyse sowie die Planung der Softwarearchitektur und der Kommunikationswege."
            ),
            "aufgaben": [
                "Erstellung eines Proof of Concept",
                "Analyse des Marktes und Ermittlung des Bedarfs",
                "Planung und Beschaffung der notwendigen Hardware",
                "Planung der Softwarearchitektur",
                "Analyse und Planung der verfügbaren Ressourcen"
                "Definition von Einflussgrößen, Datenstrukturen und Kommunikationswegen",
            ],
            "technologien": "Python, Confluence, Jira, Draw.io, Visual Paradigm",
            "von": "02/2019",
            "bis": "05/2019",
            "logo": "./static/images/schottel.png",
            "link": "https://www.schottel.de/home",
        },
        {
            "title": "Deployment Tool Einführung",
            "shortDescription": "Einführung eines Deployment Tools zum automatisierten Rollout der betriebenen Software...",
            "rolle": "Developer / Tester / PO",
            "description": (
                "Die SCHOTTEL GmbH umfasst die Propulsionsaktivitäten der SCHOTTEL-Gruppe. Sie ist gleichzeitig die Wurzel und das größte Unternehmen der heutigen SCHOTTEL-Gruppe, aus der sich seit der Gründung im Jahr 1921 ein weltweit führendes Unternehmen im Bereich der Schiffsantriebe entwickelte. Die SCHOTTEL GmbH konstruiert, produziert und vertreibt rundum steuerbare Antriebs- und Manövriersysteme sowie komplette Antriebsanlagen bis 30 MW Leistung für Schiffe aller Art und Größe. Automationssysteme und Marine Services runden die Betreuung rund um den Lebenszyklus eines Schiffs ab."
            ),
            "aufgaben": [
                "Analyse der Anforderungen und Planung der Architektur",
                "Umsetzung des Deployment Tools",
                "Schulung der Mitarbeiter",
                "Erstellung und Pflege der technischen sowie anwenderspezifischen Dokumentation",
            ],
            "technologien": "Python, Tkinter, ZeroMQ, Reddis, Debian",
            "von": "02/2018",
            "bis": "01/2019",
            "logo": "./static/images/schottel.png",
            "link": "https://www.schottel.de/home",
        },
    ]

    projects = sorted(projects, key=lambda p: parse_date(p.get("bis")), reverse=True)

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
        {"name": "CSS3", "level": "Advanced", "icon": "devicon-css3-plain"},
        {"name": "JavaScript", "level": "Advanced", "icon": "devicon-javascript-plain"},
        {
            "name": "TypeScript",
            "level": "Advanced",
            "icon": "devicon-typescript-plain",
        },  # ggf. eigenes Icon, falls verfügbar
        {"name": "React", "level": "Advanced", "icon": "devicon-react-original"},
        {"name": "Angular", "level": "Advanced", "icon": "devicon-angularjs-plain"},
        {"name": "Node.js", "level": "Intermediate", "icon": "devicon-nodejs-plain"},
        {"name": "C#", "level": "Advanced", "icon": "devicon-csharp-plain"},
        {"name": "PHP", "level": "Intermediate", "icon": "devicon-php-plain"},
        {"name": "Java", "level": "Intermediate", "icon": "devicon-java-plain"},
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
            "name": "Jenkins",
            "level": "Intermediate",
            "icon": "devicon-jenkins-plain",
        },  # falls ein Icon vorhanden ist
        {
            "name": "Dynamics 365",
            "level": "Expert",
            "icon": "static/images/dynamics.png",
        },
        {
            "name": "Prometheus",
            "level": "Intermediate",
            "icon": "devicon-prometheus-plain",
        },  # ggf. eigenes Icon
        {
            "name": "Grafana",
            "level": "Intermediate",
            "icon": "devicon-grafana-plain",
        },  # ggf. eigenes Icon
        {
            "name": "Jira",
            "level": "Intermediate",
            "icon": "devicon-jira-plain",
        },  # falls vorhanden
        {
            "name": "Confluence",
            "level": "Intermediate",
            "icon": "devicon-confluence-plain",
        },  # Platzhalter, wenn kein offizielles Icon existiert
        {"name": "Bootstrap", "level": "Advanced", "icon": "devicon-bootstrap-plain"},
        {
            "name": "Microservices",
            "level": "Advanced",
            "icon": "devicon-microservices-plain",
        },  # ggf. eigenes Icon
        {
            "name": "MQTT",
            "level": "Intermediate",
            "icon": "devicon-mqtt-plain",
        },  # ggf. eigenes Icon
        {
            "name": "ZeroMQ",
            "level": "Intermediate",
            "icon": "devicon-zeromq-plain",
        },  # ggf. eigenes Icon
        {
            "name": "Cucumber",
            "level": "Intermediate",
            "icon": "devicon-cucumber-plain",
        },  # ggf. eigenes Icon
        {
            "name": "Gherkin",
            "level": "Intermediate",
            "icon": "devicon-gherkin-plain",
        },  # ggf. eigenes Icon
        {
            "name": "TDD",
            "level": "Intermediate",
            "icon": "devicon-tdd-plain",
        },  # ggf. eigenes Icon
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
