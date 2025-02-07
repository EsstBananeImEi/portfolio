from datetime import datetime
import json
from pathlib import Path
from typing import TypeVar, Type, List

T = TypeVar("T")


def parse_date(date_str):
    """
    Wandelt einen Datums-String in ein datetime-Objekt um.
    Unterstützte Formate:
    - MM/YYYY
    - DD.MM.YYYY

    Falls der String "Aktuell" (unabhängig von Groß-/Kleinschreibung) lautet, wird datetime.now() zurückgegeben.
    Falls der String None oder ein ungültiges Format ist, wird ein sehr altes Datum zurückgegeben,
    sodass das Projekt beim Sortieren hinten einsortiert wird.
    """
    if not date_str:
        return datetime.min
    if date_str.lower() == "aktuell":
        return datetime.now()

    for fmt in ("%m/%Y", "%d.%m.%Y"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    return datetime.min


def load_json(filepath: str) -> dict:
    with open(Path(filepath), encoding="utf-8") as f:
        return json.load(f)


def load_data(cls: Type[T], filepath: str) -> T:
    data = load_json(f"app/data/{filepath}")
    return cls(**data)


def load_data_list(cls: Type[T], filepath: str) -> List[T]:
    data_list = load_json(f"app/data/{filepath}")
    return [cls(**data) for data in data_list]
