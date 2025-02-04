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
        {
            "name": "Python",
            "level": "Expert",
            "icon": "devicon-python-plain",
            "info": "Dynamisch, vielseitig und weit verbreitet.",
            "description": "Python ist eine leistungsstarke, interpretierte Programmiersprache, die sich besonders für Skripting, Automatisierung und Datenanalyse eignet.",
            "link": "https://www.python.org/",
        },
        {
            "name": "Flask",
            "level": "Intermediate",
            "icon": "devicon-flask-original",
            "info": "Ein leichtgewichtiges Webframework.",
            "description": "Flask ist ein minimalistisches Python-Webframework, das sich hervorragend für schnelle Prototypen und kleine bis mittelgroße Webanwendungen eignet.",
            "link": "https://flask.palletsprojects.com/",
        },
        {
            "name": "HTML5",
            "level": "Advanced",
            "icon": "devicon-html5-plain",
            "info": "Standard zur Strukturierung von Webinhalten.",
            "description": "HTML5 ist die neueste Version der Hypertext Markup Language, die zur Strukturierung und Darstellung von Inhalten im Web dient.",
            "link": "https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5",
        },
        {
            "name": "CSS3",
            "level": "Advanced",
            "icon": "devicon-css3-plain",
            "info": "Gestaltung und Layout von Webseiten.",
            "description": "CSS3 ermöglicht die Gestaltung von Webseiten mit modernen Layout- und Animationstechniken.",
            "link": "https://developer.mozilla.org/en-US/docs/Web/CSS",
        },
        {
            "name": "JavaScript",
            "level": "Advanced",
            "icon": "devicon-javascript-plain",
            "info": "Die Sprache des Webs.",
            "description": "JavaScript ist eine vielseitige Sprache, die sowohl auf der Client- als auch auf der Serverseite eingesetzt wird.",
            "link": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
        },
        {
            "name": "TypeScript",
            "level": "Advanced",
            "icon": "devicon-typescript-plain",
            "info": "JavaScript mit Typisierung.",
            "description": "TypeScript erweitert JavaScript um statische Typisierung und moderne Features, um große Codebasen besser verwalten zu können.",
            "link": "https://www.typescriptlang.org/",
        },
        {
            "name": "React",
            "level": "Advanced",
            "icon": "devicon-react-original",
            "info": "Eine Bibliothek zur Erstellung von UI-Komponenten.",
            "description": "React ist eine JavaScript-Bibliothek zur Erstellung von wiederverwendbaren UI-Komponenten und Single-Page-Anwendungen.",
            "link": "https://reactjs.org/",
        },
        {
            "name": "Angular",
            "level": "Advanced",
            "icon": "devicon-angularjs-plain",
            "info": "Ein Framework für dynamische Webanwendungen.",
            "description": "Angular ist ein leistungsstarkes Framework für den Aufbau von dynamischen und modularen Webanwendungen.",
            "link": "https://angular.io/",
        },
        {
            "name": "Node.js",
            "level": "Intermediate",
            "icon": "devicon-nodejs-plain",
            "info": "Serverseitiges JavaScript.",
            "description": "Node.js ermöglicht die Ausführung von JavaScript auf dem Server und ist ideal für skalierbare Netzwerkapplikationen.",
            "link": "https://nodejs.org/",
        },
        {
            "name": "C#",
            "level": "Advanced",
            "icon": "devicon-csharp-plain",
            "info": "Eine moderne, objektorientierte Programmiersprache.",
            "description": "C# wird häufig für die Entwicklung von Windows-Anwendungen und Spielen eingesetzt, etwa mit Unity.",
            "link": "https://docs.microsoft.com/en-us/dotnet/csharp/",
        },
        {
            "name": "PHP",
            "level": "Intermediate",
            "icon": "devicon-php-plain",
            "info": "Eine weit verbreitete serverseitige Sprache.",
            "description": "PHP wird hauptsächlich zur Erstellung dynamischer Webseiten und Webanwendungen verwendet.",
            "link": "https://www.php.net/",
        },
        {
            "name": "Java",
            "level": "Intermediate",
            "icon": "devicon-java-plain",
            "info": "Eine universell einsetzbare Programmiersprache.",
            "description": "Java ist bekannt für seine Plattformunabhängigkeit und wird in vielen Unternehmensanwendungen eingesetzt.",
            "link": "https://www.java.com/",
        },
        {
            "name": "Docker",
            "level": "Intermediate",
            "icon": "devicon-docker-plain",
            "info": "Containerisierung von Anwendungen.",
            "description": "Docker ermöglicht es, Anwendungen in Containern zu isolieren, was die Bereitstellung und Skalierung vereinfacht.",
            "link": "https://www.docker.com/",
        },
        {
            "name": "Git",
            "level": "Advanced",
            "icon": "devicon-git-plain",
            "info": "Versionskontrolle für Projekte.",
            "description": "Git ist ein verteiltes Versionskontrollsystem, das es Teams ermöglicht, effizient an Code zu arbeiten.",
            "link": "https://git-scm.com/",
        },
        {
            "name": "Linux",
            "level": "Advanced",
            "icon": "devicon-linux-plain",
            "info": "Ein vielseitiges Betriebssystem.",
            "description": "Linux ist ein Open-Source-Betriebssystem, das für seine Stabilität und Sicherheit bekannt ist.",
            "link": "https://www.linux.org/",
        },
        {
            "name": "MySQL",
            "level": "Intermediate",
            "icon": "devicon-mysql-plain",
            "info": "Relationale Datenbank.",
            "description": "MySQL ist eine der bekanntesten relationalen Datenbanken und wird häufig in Webanwendungen eingesetzt.",
            "link": "https://www.mysql.com/",
        },
        {
            "name": "PostgreSQL",
            "level": "Intermediate",
            "icon": "devicon-postgresql-plain",
            "info": "Fortschrittliche relationale Datenbank.",
            "description": "PostgreSQL ist eine leistungsstarke, objektrelationale Datenbank, die für ihre Stabilität und Erweiterbarkeit bekannt ist.",
            "link": "https://www.postgresql.org/",
        },
        {
            "name": "SQLite",
            "level": "Advanced",
            "icon": "devicon-sqlite-plain",
            "info": "Leichte, dateibasierte Datenbank.",
            "description": "SQLite ist eine serverlose, selbst enthaltene SQL-Datenbank, die sich gut für kleinere Projekte eignet.",
            "link": "https://www.sqlite.org/",
        },
        {
            "name": "Jenkins",
            "level": "Intermediate",
            "icon": "devicon-jenkins-plain",
            "info": "Automatisierung von CI/CD-Prozessen.",
            "description": "Jenkins ist ein Open-Source-Automatisierungsserver, der hilft, den Softwareentwicklungsprozess zu automatisieren.",
            "link": "https://www.jenkins.io/",
        },
        {
            "name": "Dynamics 365",
            "level": "Expert",
            "icon": "static/images/dynamics.png",
            "info": "Enterprise-CRM und ERP-Lösungen.",
            "description": "Dynamics 365 bietet eine umfassende Suite von Unternehmensanwendungen, die CRM und ERP integrieren.",
            "link": "https://dynamics.microsoft.com/",
        },
        {
            "name": "Prometheus",
            "level": "Intermediate",
            "icon": "devicon-prometheus-plain",
            "info": "Monitoring und Alerting-System.",
            "description": "Prometheus ist ein Open-Source-Monitoring- und Alerting-Toolkit, das besonders in Cloud-Umgebungen beliebt ist.",
            "link": "https://prometheus.io/",
        },
        {
            "name": "Grafana",
            "level": "Intermediate",
            "icon": "devicon-grafana-plain",
            "info": "Visualisierung von Metriken und Logs.",
            "description": "Grafana wird häufig zusammen mit Prometheus verwendet, um Metriken in ansprechenden Dashboards darzustellen.",
            "link": "https://grafana.com/",
        },
        {
            "name": "Jira",
            "level": "Intermediate",
            "icon": "devicon-jira-plain",
            "info": "Projektmanagement und Issue-Tracking.",
            "description": "Jira ist ein Tool zur Verwaltung von Projekten, Aufgaben und Bugs, das vor allem in agilen Teams eingesetzt wird.",
            "link": "https://www.atlassian.com/software/jira",
        },
        {
            "name": "Confluence",
            "level": "Intermediate",
            "icon": "devicon-confluence-plain",
            "info": "Wissensmanagement und Zusammenarbeit.",
            "description": "Confluence ist ein Kollaborationswerkzeug, mit dem Teams Dokumente, Notizen und Projektpläne gemeinsam bearbeiten können.",
            "link": "https://www.atlassian.com/software/confluence",
        },
        {
            "name": "Bootstrap",
            "level": "Advanced",
            "icon": "devicon-bootstrap-plain",
            "info": "CSS-Framework für responsives Design.",
            "description": "Bootstrap vereinfacht die Entwicklung von responsiven und modernen Webseiten durch vordefinierte Komponenten und Styles.",
            "link": "https://getbootstrap.com/",
        },
        {
            "name": "Microservices",
            "level": "Advanced",
            "icon": "static/images/microservice.png",
            "info": "Architekturstil für skalierbare Anwendungen.",
            "description": "Microservices teilen Anwendungen in kleine, unabhängige Services auf, die jeweils eine einzelne Funktion übernehmen.",
            "link": "https://microservices.io/",
        },
        {
            "name": "MQTT",
            "level": "Intermediate",
            "icon": "static/images/mqtt.png",
            "info": "Leichtgewichtiges Messaging-Protokoll für IoT.",
            "description": "MQTT ist ein Publish/Subscribe-Protokoll, das sich hervorragend für die Kommunikation in IoT-Anwendungen eignet.",
            "link": "http://mqtt.org/",
        },
        {
            "name": "ZeroMQ",
            "level": "Intermediate",
            "icon": "static/images/zeromq.png",
            "info": "Asynchrone Messaging-Bibliothek.",
            "description": "ZeroMQ ist eine leistungsfähige Messaging-Bibliothek, die beim Aufbau verteilter Systeme hilft.",
            "link": "https://zeromq.org/",
        },
        {
            "name": "Cucumber",
            "level": "Intermediate",
            "icon": "static/images/cucumber.png",
            "info": "BDD-Tool zur Testautomatisierung.",
            "description": "Cucumber nutzt Gherkin-Syntax, um Anforderungen als leicht verständliche Szenarien zu beschreiben, und automatisiert diese als Tests.",
            "link": "https://cucumber.io/",
        },
        {
            "name": "Gherkin",
            "level": "Intermediate",
            "icon": "static/images/gherkin.svg",
            "info": "Spezifikationssprache für BDD.",
            "description": "Gherkin ist eine domänenspezifische Sprache, die es ermöglicht, Anforderungen in verständlichen Szenarien zu beschreiben.",
            "link": "https://cucumber.io/docs/gherkin/reference/",
        },
        {
            "name": "TDD",
            "level": "Intermediate",
            "icon": "static/images/tdd.svg",
            "info": "Test-Driven Development als Entwicklungsansatz.",
            "description": "TDD ist ein Entwicklungsprozess, bei dem Tests vor dem eigentlichen Code geschrieben werden, um so die Implementierung zu leiten.",
            "link": "https://www.agilealliance.org/glossary/tdd/",
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
