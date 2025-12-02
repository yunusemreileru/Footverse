# M02_settings/utils/theme_registry.py
import os
import json
from django.conf import settings

THEME_PRESET_PATH = os.path.join(settings.BASE_DIR, "theme_presets")
THEME_PRESET_PATH = os.path.abspath(THEME_PRESET_PATH)
THEME_SCHEMA_FILENAME = "theme_schema.json"


def load_theme_json(theme_code: str) -> dict:
    """
    Verilen theme_code için JSON dosyasını okur.
    Bulamazsa footverse_default'e düşer.
    """
    file_path = os.path.join(THEME_PRESET_PATH, f"{theme_code}.json")

    if not os.path.exists(file_path):
        file_path = os.path.join(THEME_PRESET_PATH, "footverse_default.json")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def get_available_themes():
    """
    theme_presets klasöründeki tüm presetleri döndürür.
    Her eleman: {"code": "...", "name": "..."}
    theme_schema.json hariç tutulur.
    """
    if not os.path.isdir(THEME_PRESET_PATH):
        return []

    themes = []

    for fname in os.listdir(THEME_PRESET_PATH):
        if not fname.endswith(".json"):
            continue
        if fname == THEME_SCHEMA_FILENAME:
            continue

        full_path = os.path.join(THEME_PRESET_PATH, fname)

        try:
            with open(full_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            meta = data.get("meta", {})
            code = meta.get("code") or fname.replace(".json", "")
            name = meta.get("name") or code.replace("_", " ").title()

            themes.append({"code": code, "name": name})
        except Exception:
            continue

    themes.sort(key=lambda x: x["name"].lower())
    return themes
