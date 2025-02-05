
<p align="center">
    <img src="/app/static/images/LOGONEU.svg" width="256"/>
</p>
t
# 🌟 Portfolio Webanwendung  

Diese moderne und interaktive **Portfolio-Webanwendung** wurde mit **Flask** entwickelt und ermöglicht es, persönliche Projekte, Fähigkeiten und Kontaktinformationen ansprechend darzustellen.  

✨ **Highlights:**  

- Entwickelt mit **Flask** und **Jinja2 Templates**  
- **Responsives Design** mit **Tailwind CSS** und **Alpine.js**  
- **Einfache Bereitstellung** über **Render** oder **Heroku**  
- **Kontaktmöglichkeiten** per E-Mail, LinkedIn und GitHub  

🚀 Die Anwendung bietet ein modernes UI-Erlebnis mit interaktiven Komponenten und ist ideal für Entwickler, die ihre Projekte professionell präsentieren möchten.  

---

## Features

- ✅ Responsives Design mit Tailwind CSS  
- ✅ Dynamische Projektanzeige mit interaktiven Kacheln  
- ✅ Integration von GitHub-Projekten  
- ✅ Anpassbare Skills-Übersicht  
- ✅ Kontaktmöglichkeiten (E-Mail, LinkedIn, GitHub)  
- ✅ Deployment über [Render](https://render.com/) oder Heroku möglich  

---

## 📂 Projektstruktur

```
portfolio-main/
│-- app/                # Hauptverzeichnis der Flask-App
│   │-- templates/      # HTML-Templates
│   │-- static/         # Statische Dateien (CSS, JS, Bilder)
│   │-- routes.py       # Routen-Definitionen
│   │-- models.py       # Datenbank-Modelle (falls genutzt)
│   │-- __init__.py     # Initialisierung der Flask-App
│-- config.py           # Konfigurationsdatei
│-- run.py              # Startpunkt der Anwendung
│-- LICENSE             # Lizenz-Datei
│-- requirements.txt    # Abhängigkeiten
│-- Procfile            # Deployment-Datei für Render/Heroku
│-- .gitignore          # Dateien, die nicht getrackt werden sollen
```

---

## 🛠 Installation & Lokale Entwicklung

### 1️⃣ Voraussetzungen

- Python 3.x
- Virtualenv (optional)
- (Optional) Github Repository für das Portfolio um das Deployment über Render zu ermöglichen

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

Die Anwendung läuft dann unter `http://127.0.0.1:5000/`

---

## 🌍 Deployment (Render)

### 1. Repository zu Render hochladen

Erstelle ein Repository auf GitHub und pushe den Code:

```sh
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/dein-benutzername/dein-repo.git
git push -u origin main
```

Erstelle ein Konto bei [Render](https://render.com/) und erstelle einen neuen Web Service, um dein Repository zu verbinden.

### 2. `Procfile` für Render

Erstelle eine Datei namens `Procfile` im Root-Verzeichnis mit folgendem Inhalt:

```sh
web: gunicorn run:app
```

Render erkennt dieses `Procfile` und startet den Server mit Gunicorn.

---

## 🛡 Sicherheitshinweise

- **Umgebungsvariablen:** Sensible Daten wie API-Keys oder Zugangsdaten sollten nicht im Code gespeichert, sondern als Umgebungsvariablen definiert werden.
- **Abhängigkeiten aktuell halten:** Stelle sicher, dass du regelmäßig `pip list --outdated` nutzt und Updates durchführst.
- **HTTPS verwenden:** Falls das Projekt öffentlich zugänglich ist, sollte HTTPS verwendet werden.

---

## 🔍 Fehlerbehebung

| Problem | Lösung |
|---------|---------|
| **ModuleNotFoundError** | Stelle sicher, dass du alle Abhängigkeiten installiert hast: `pip install -r requirements.txt` |
| **Port bereits belegt** | Nutze einen anderen Port: `flask run --port=5001` |
| **Fehlende statische Dateien** | Überprüfe den Pfad in `templates/` und `static/` |
| **Render zeigt Fehler 502** | Überprüfe das `Procfile` und den Startbefehl |

---

## 🎉 Beitragen & Verbesserungsvorschläge

Falls du Verbesserungsvorschläge oder Features hinzufügen möchtest:

1. Erstelle ein Issue in diesem Repository.
2. Forke das Repository und erstelle einen neuen Branch.
3. Mache deine Änderungen und erstelle einen Pull-Request.

---

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Weitere Informationen findest du in der [Lizenzdatei](LICENSE).

---
