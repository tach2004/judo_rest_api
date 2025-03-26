import json
import os

STORAGE_PATH = "/config/custom_components/judo_rest_api/judo_storage.json"

# Liste der Entitäten, die gespeichert werden sollen (nur hier anpassen!)
PERSISTENT_ENTITIES = ["sleep_mode_duration", "holiday_mode_write"]

def save_last_written_value(key: str, value: str):
    """Speichert den letzten geschriebenen Wert in der JSON-Datei."""
    if key not in PERSISTENT_ENTITIES:
        return  # Nur speichern, wenn die Entität in der Liste ist

    data = load_last_written_values()  # Vorhandene Werte laden
    data[key] = value  # Neuen Wert speichern
    with open(STORAGE_PATH, "w") as file:
        json.dump(data, file)

def load_last_written_values():
    """Lädt die gespeicherten Werte aus der JSON-Datei."""
    if not os.path.exists(STORAGE_PATH):
        return {}  # Falls Datei nicht existiert, leeres Dict zurückgeben
    try:
        with open(STORAGE_PATH, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}  # Falls Datei beschädigt ist, leeres Dict zurückgeben
