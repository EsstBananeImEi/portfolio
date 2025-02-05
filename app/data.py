from datetime import datetime
import json
import os


def parse_date(date_str):
    """
    Wandelt einen Datums-String im Format MM/YYYY in ein datetime-Objekt um.
    Falls der String "Aktuell" (unabhängig von Groß-/Kleinschreibung) lautet, wird datetime.now() zurückgegeben.
    Falls der String None oder ein ungültiges Format ist, wird ein sehr altes Datum zurückgegeben,
    sodass das Projekt beim Sortieren hinten einsortiert wird.
    """
    if not date_str:
        return datetime.min
    if date_str.lower() == "aktuell":
        return datetime.now()
    try:
        return datetime.strptime(date_str, "%m/%Y")
    except ValueError:
        return datetime.min

def group_skills(skills):
    grouped = {}
    for skill in skills:
        # Nutze das "group"-Feld; falls es nicht vorhanden ist, gruppiere unter "Other"
        group = skill.get("group", "Other")
        grouped.setdefault(group, []).append(skill)
    return grouped

def load_projects(filename: str):
    """
    Lädt die Projektdaten aus der JSON-Datei und gibt sie als Liste von Dictionaries zurück.
    Die JSON-Datei wird hier relativ zu diesem Modul erwartet: z.b app/data/projects.json
    """
    json_path = os.path.join(os.path.dirname(__file__), "data", filename)
    with open(json_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)
    return json_data
