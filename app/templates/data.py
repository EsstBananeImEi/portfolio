from datetime import datetime


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
