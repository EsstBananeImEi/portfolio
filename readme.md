<p align="center">
    <img src="/app/static/images/LOGONEU.svg" width="256"/>
</p>



# Portfolio Webanwendung

Diese moderne und interaktive Portfolio-Webanwendung wurde mit Flask und Jinja2 entwickelt und bietet Entwicklern eine ansprechende Plattform, um Projekte, Fähigkeiten und Kontaktinformationen professionell zu präsentieren. Dank eines responsiven Designs mit Tailwind CSS und interaktiven Komponenten via Alpine.js überzeugt die Anwendung durch ihre klare Struktur und Benutzerfreundlichkeit. Ideal für den Einsatz auf modernen Deployment-Plattformen wie Render oder Heroku, ermöglicht sie eine unkomplizierte Bereitstellung und Wartung.
 
## ✨ Highlights

- Entwickelt mit **Flask** und **Jinja2 Templates**  
- **Responsives Design** mit **Tailwind CSS** und **Alpine.js**  
- **Einfache Bereitstellung** über **Render** oder **Heroku**  
- **Konfigurierbare Inhalte** – Alle wichtigen Informationen (Kontakt, About, Skills, Projekte) werden über externe JSON-Dateien verwaltet  
- **Kontaktmöglichkeiten** per E-Mail, LinkedIn und GitHub  

🚀 Die Anwendung bietet ein modernes UI-Erlebnis mit interaktiven Komponenten und ist ideal für Entwickler, die ihre Projekte professionell präsentieren möchten.

---

## ✅ Features

- Responsives Design mit Tailwind CSS  
- Dynamische Projektanzeige mit interaktiven Kacheln  
- Integration von GitHub-Projekten  
- Anpassbare Skills-Übersicht  
- Kontaktmöglichkeiten (E-Mail, LinkedIn, GitHub)  
- **Konfiguration der Website-Inhalte über externe JSON-Dateien**  
- Deployment über [Render](https://render.com/) oder Heroku möglich  

---

## 📂 Projektstruktur

```
portfolio-main/
│-- app/                        # Hauptverzeichnis der Flask-App
│   │-- templates/              # HTML-Templates
│   │-- static/                 # Statische Dateien (CSS, JS, Bilder)
│   │-- routes.py               # Routen-Definitionen
│   │-- models.py               # Datenbank-Modelle (falls genutzt)
│   │-- __init__.py             # Initialisierung der Flask-App
│-- data/                       # Externe JSON-Dateien für konfigurierbare Inhalte
│   │-- about.json              # Kontaktinformationen
│   │-- contact.json            # "Über mich"-Informationen
│   │-- github_projects.json    # "Über mich"-Informationen
│   │-- projects.json           # "Über mich"-Informationen
│   │-- skills.json             # "Über mich"-Informationen
│-- config.py                   # Konfigurationsdatei
│-- run.py                      # Startpunkt der Anwendung
│-- LICENSE                     # Lizenz-Datei
│-- requirements.txt            # Abhängigkeiten
│-- Procfile                    # Deployment-Datei für Render/Heroku
│-- .gitignore                  # Dateien, die nicht getrackt werden sollen
```

---

## 🔧 JSON-Konfiguration

### **data/contact.json**

```json
{
    "vorname": "Max",
    "nachname": "Mustermann",
    "email": "mustermann@email.de",
    "linkedin": "https://www.linkedin.com/in/mustermann/",
    "github": "https://github.com/mustermannsRepo",
    "profile_image": "images/mustermannProfilbild.jpg"
}
```

- profile_image: Enthält den relativen Pfad zum Profilbild, das über Flask mittels url_for('static', filename=...) eingebunden wird.

### **data/about.json**

```json
{
    "greeting": "Hallo, ich bin Max!",
    "bio": "Als XXX habe ich mich auf YYY spezialisiert und bringe ZZZ Jahre " +
            "Erfahrung in der Entwicklung von .....",
    "role": "Rolle XYZ",
}
```

- bio: Der komplette Text wird als ein einziger String gespeichert. Falls zusätzliche Zeilenumbrüche benötigt werden, können diese mit \n eingefügt werden.

### **data/github_projects.json**

```json
[
    {
        "title": "Projekt 1",
        "shortDescription": "Hier kommt eine kurze Beschreibung des Projekts hin.",
        "description": "Hier kommt eine ausführliche Beschreibung des Projekts hin.",
        "link": "Link zum GitHub-Repository",
        "technologien": "Technologie 1, Technologie 2, Technologie 3",
        "logo": "./static/images/projekt1.png",
        "wip": false // true, falls das Projekt noch in Arbeit ist
    },
    // Weitere Projekte
]
```

### **data/projects.json**

```json
[
    {
    "title": "Projektbeispiel",
    "shortDescription": "kurze Beschreibung des Projekts",
    "rolle": "Entwickler",
    "description": "Ausführliche Beschreibung des Projekts.",
    "aufgaben": [
        "Aufgabe 1",
        "Aufgabe 2",
        "Aufgabe 3"
    ],
    "technologien": "Technologien nach Bedarf",
    "von": "mm/yyyy",
    "bis": "mm/yyyy",
    "logo": "./static/images/placeholder.png",
    "link": "www.projektbeispiel.de"
    },
    // Weitere Projekte
]
```

### **data/skills.json**

```json
[
    {
        "name": "Skill 1",
        "level": "Skill-Level", // z.B. "Fortgeschritten"
        "icon": "devicon-python-plain", // Icon-Klasse (z.B. devicon-python-plain oder static/images/python.png wenn kein icon auf devicon.io vorhanden ist)
        "info": "Kurze Beschreibung des Skills",
        "description": "Ausführliche Beschreibung des Skills",
        "link": "Link zu einer beliebige Ressource (z.B. Dokumentation)"
    },
    // Weitere Skills
]
```

---

## 🛠 Installation & Lokale Entwicklung

### 1️⃣ Voraussetzungen

- Python 3.x
- Virtualenv (optional)
- (Optional) GitHub Repository für das Portfolio, um das Deployment über Render zu ermöglichen

### 2️⃣ Installation

```sh
# Repository klonen
git clone <repository-url>
cd portfolio-main

# Virtuelle Umgebung erstellen
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Abhängigkeiten installieren
pip install -r requirements.txt
```

### 3️⃣ Start der Anwendung

```sh
python run.py
```

Die Anwendung läuft dann unter `http://127.0.0.1:5000/`.

---

## 🌍 Deployment (Render)

1. Repository auf GitHub hochladen:

```sh
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/dein-benutzername/dein-repo.git
git push -u origin main
```

2. Bei [Render](https://render.com/) anmelden und ein neues Web Service mit dem Repository verbinden.

3. `Procfile` für Render erstellen:

```sh
web: gunicorn run:app
```

---

## 🛡 Sicherheitshinweise

- **Umgebungsvariablen:** API-Keys oder Zugangsdaten nicht im Code speichern, sondern als Umgebungsvariablen definieren.
- **Abhängigkeiten aktuell halten:** Regelmäßig `pip list --outdated` nutzen und Updates durchführen.
- **HTTPS verwenden:** Falls das Projekt öffentlich zugänglich ist, sollte HTTPS verwendet werden.

---

## 🔍 Fehlerbehebung

| Problem                     | Lösung                                                        |
|-----------------------------|----------------------------------------------------------------|
| **ModuleNotFoundError**     | `pip install -r requirements.txt` ausführen                  |
| **Port bereits belegt**     | `flask run --port=5001` nutzen                                |
| **Fehlende statische Dateien** | Überprüfe den Pfad in `templates/` und `static/`            |
| **Render zeigt Fehler 502** | Überprüfe das `Procfile` und den Startbefehl                  |

---

## 🎉 Beitragen & Verbesserungsvorschläge

Falls du Verbesserungsvorschläge oder Features hinzufügen möchtest:

1. Erstelle ein Issue in diesem Repository.
2. Forke das Repository und erstelle einen neuen Branch.
3. Mache deine Änderungen und erstelle einen Pull-Request.

---

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Weitere Informationen findest du in der [Lizenzdatei](LICENSE).
