
```markdown
# Portfolio-Projekt

Dies ist ein Portfolio-Projekt, das eine Webanwendung basierend auf **Flask** und **Tailwind CSS** darstellt.  
Das Projekt enthält Konfigurationen für `gunicorn` und ist für das Deployment auf **Heroku** vorbereitet.  

---

## 📁 Projektstruktur

```python
portfolio-main/
├── .gitignore
├── Procfile                 # Heroku-Prozessdatei (für gunicorn)
├── config.py                # Konfigurationsdatei (muss evtl. angepasst werden)
├── requirements.txt          # Liste der Python-Abhängigkeiten
├── run.py                    # Startpunkt der Flask-Anwendung
├── .vscode/
│   └── settings.json
├── app/
│   ├── __init__.py           # Initialisiert die Flask-App
│   ├── models.py             # Datenbankmodelle (falls genutzt)
│   ├── routes.py             # Definiert die API-Routen
│   ├── static/               # Statische Assets (CSS, JS, Bilder)
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── images/           # Logos & Bilder für die Website
│   │   ├── js/
│   │   │   ├── main.js
│   │   │   ├── tailwind-config.js
│   ├── templates/            # HTML-Vorlagen
│   │   ├── base.html
│   │   ├── data.py           # Hier werden Projekte & Skills definiert
│   │   ├── index.html
│   │   └── partials/         # Gemeinsame UI-Komponenten
│   │       ├── footer.html
│   │       └── nav.html
```

---

## 📌 **Wie werden Projekte festgelegt?**  

Die **Projekte** werden im **`data.py`** definiert.  
Hier werden sie als Liste von **Dictionaries** gespeichert, die alle relevanten Informationen enthalten.  

📌 **Beispiel für ein Projekt in `data.py`**  

```python
projects = [
    {
        "title": "Mein Portfolio",
        "description": "Eine persönliche Portfolio-Website mit Flask & Tailwind CSS.",
        "image": "static/images/portfolio.png",
        "link": "https://mein-portfolio.com"
    },
    {
        "title": "IoT Dashboard",
        "description": "Ein Dashboard zur Visualisierung von IoT-Sensordaten.",
        "image": "static/images/iot-dashboard.png",
        "link": "https://iot-dashboard.com"
    }
]
```

📌 **Wie werden neue Projekte hinzugefügt?**  
- Öffne die Datei **`router.py`**  
- Füge ein weiteres Dictionary zur **`projects`**-Liste hinzu  
- Achte darauf, dass `title`, `description`, `image` und `link` korrekt angegeben sind  

---

## 📌 **Wie sind die Skills aufgebaut und wie funktionieren sie?**  

Die **Skills** werden ebenfalls in **`router.py`** gespeichert.  
Sie bestehen aus einer **Liste von Kategorien**, wobei jede Kategorie eine Liste von Skills enthält.  

📌 **Beispiel für den Skill-Aufbau in `data.py`**  

```python
skills = {
    "Programming Languages": ["Python", "JavaScript", "Java", "C++"],
    "Frameworks": ["Flask", "Django", "React", "Vue.js"],
    "Tools & Technologies": ["Docker", "Git", "CI/CD", "Kubernetes"],
    "Soft Skills": ["Teamwork", "Problem Solving", "Communication"]
}
```

📌 **Wie werden neue Skills hinzugefügt?**  
- Öffne **`router.py`**  
- Füge eine neue Kategorie oder einen neuen Skill innerhalb einer vorhandenen Kategorie hinzu  

📌 **Wie werden die Skills auf der Website angezeigt?**  
- Die Skills werden in **`index.html`** mithilfe einer Schleife über die `skills`-Datenstruktur generiert  
- Falls eine Kategorie fehlt oder falsch angezeigt wird, überprüfe `data.py`  

---

## 🔧 **Installation & Setup**  

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

## 🚀 **Deployment mit Gunicorn & Heroku**  

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

## 🔄 **Anpassbare Einstellungen**  

Einige Daten müssen für den individuellen Gebrauch angepasst werden:

### **1️⃣ `config.py`**  
Hier werden möglicherweise Umgebungsvariablen oder API-Keys gespeichert, die du ändern musst.

### **2️⃣ Statische Inhalte**  
Falls du eigene Bilder oder Logos einfügen möchtest, ersetze die Dateien im Verzeichnis:
```
app/static/images/
```

### **3️⃣ HTML-Vorlagen (`templates/`)**  
- Passe `index.html` an, um persönliche Inhalte anzuzeigen  
- Ändere `partials/nav.html`, um eigene Menüpunkte hinzuzufügen  

---

## 🛠 **Technologien & Tools**  

- **Backend**: Flask (Python)  
- **Frontend**: Tailwind CSS, JavaScript  
- **WSGI-Server**: Gunicorn  
- **Deployment**: Heroku (über `Procfile` konfiguriert)  
- **Datenbank**: (Falls vorhanden, bitte ergänzen)  

---

## 📄 **Lizenz**  

Dieses Projekt unterliegt der **[Lizenzname]** (falls zutreffend).  
Bitte ergänzen oder entfernen, falls nicht relevant.

---

Falls du noch Änderungen brauchst, sag einfach Bescheid!  
Diese README enthält nun alle wichtigen Infos zu **Projekten, Skills, Gunicorn & Deployment** und ist **sauber formatiert**.