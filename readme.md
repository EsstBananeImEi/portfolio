Danke für dein Feedback! Ich werde die Projektstruktur noch einmal klarer formatieren und die gewünschten Informationen zu `gunicorn` sowie zu den individuell anpassbaren Daten hinzufügen.  

---

### **📌 Überarbeitete README.md**

```markdown
# Portfolio-Projekt

Dies ist ein Portfolio-Projekt, das eine Webanwendung basierend auf Flask und Tailwind CSS darstellt.  
Das Projekt enthält Konfigurationen für `gunicorn` und ist für das Deployment auf **Heroku** vorbereitet.  

---

## 📁 Projektstruktur

```
portfolio-main/
│── .gitignore
│── Procfile                 # Heroku-Prozessdatei (für gunicorn)
│── config.py                # Konfigurationsdatei (muss evtl. angepasst werden)
│── requirements.txt          # Liste der Python-Abhängigkeiten
│── run.py                    # Startpunkt der Flask-Anwendung
│── .vscode/
│   └── settings.json
│── app/
│   │── __init__.py           # Initialisiert die Flask-App
│   │── models.py             # Datenbankmodelle (falls genutzt)
│   │── routes.py             # Definiert die API-Routen
│   │── static/               # Statische Assets (CSS, JS, Bilder)
│   │   │── css/
│   │   │   └── style.css
│   │   │── images/           # Logos & Bilder für die Website
│   │   │── js/
│   │   │   ├── main.js
│   │   │   ├── tailwind-config.js
│   │── templates/            # HTML-Vorlagen
│       │── base.html
│       │── data.py
│       │── index.html
│       └── partials/         # Gemeinsame UI-Komponenten
│           │── footer.html
│           └── nav.html
```

---

## 🔧 Installation & Setup

### **1️⃣ Repository klonen**
```bash
git clone <REPO_URL>
cd portfolio-main
```

### **2️⃣ Virtuelle Umgebung erstellen & aktivieren**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### **3️⃣ Abhängigkeiten installieren**
```bash
pip install -r requirements.txt
```

### **4️⃣ Anwendung lokal starten**
```bash
python run.py
```

---

## 🚀 Deployment mit Gunicorn & Heroku

Die Anwendung kann mit `gunicorn` als WSGI-Server betrieben werden, was für das Deployment empfohlen wird.

### **1️⃣ Gunicorn lokal testen**
Falls `gunicorn` nicht installiert ist, installiere es mit:
```bash
pip install gunicorn
```
Dann starte die App mit:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```
- `-w 4`: Startet 4 Worker-Prozesse  
- `-b 0.0.0.0:8000`: Bindet die Anwendung an Port 8000  

### **2️⃣ Deployment auf Heroku**
Heroku nutzt das `Procfile`, um die App mit `gunicorn` zu starten:
```txt
web: gunicorn run:app
```
Um das Projekt auf **Heroku** bereitzustellen:
```bash
heroku create <app-name>
git push heroku main
heroku open
```

---

## 🔄 Anpassbare Einstellungen  

Einige Daten müssen für den individuellen Gebrauch angepasst werden:

1️⃣ **`config.py`**  
Hier werden möglicherweise Umgebungsvariablen oder API-Keys gespeichert, die du ändern musst.

2️⃣ **Statische Inhalte**  
Falls du eigene Bilder oder Logos einfügen möchtest, ersetze die Dateien im Verzeichnis:
```
app/static/images/
```

3️⃣ **HTML-Vorlagen (`templates/`)**  
- Passe `index.html` an, um persönliche Inhalte anzuzeigen  
- Ändere `partials/nav.html`, um eigene Menüpunkte hinzuzufügen  

---

## 🛠 Technologien & Tools

- **Backend**: Flask (Python)
- **Frontend**: Tailwind CSS, JavaScript
- **WSGI-Server**: Gunicorn
- **Deployment**: Heroku (über `Procfile` konfiguriert)
- **Datenbank**: (Falls vorhanden, bitte ergänzen)

---

## 📄 Lizenz

Dieses Projekt unterliegt der **[Lizenzname]** (falls zutreffend).  
Bitte ergänzen oder entfernen, falls nicht relevant.

---
