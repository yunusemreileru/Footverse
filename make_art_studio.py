import os

BASE_DIR = os.path.join("M03_art_studio")

# Klasör yapısı
DIRS = [
    BASE_DIR,
    f"{BASE_DIR}/models",
    f"{BASE_DIR}/services",
    f"{BASE_DIR}/utils",
    f"{BASE_DIR}/factories",
    f"{BASE_DIR}/views",
    f"{BASE_DIR}/templates",
    f"{BASE_DIR}/templates/M03_art_studio",
    f"{BASE_DIR}/static",
    f"{BASE_DIR}/static/M03_art_studio",
    f"{BASE_DIR}/static/M03_art_studio/css",
    f"{BASE_DIR}/static/M03_art_studio/js",
    f"{BASE_DIR}/static/M03_art_studio/img",
    f"{BASE_DIR}/static/M03_art_studio/img/shapes",
    f"{BASE_DIR}/static/M03_art_studio/img/icons",
]

# Boş Python dosyaları
PY_FILES = {
    f"{BASE_DIR}/__init__.py": "",
    f"{BASE_DIR}/apps.py": "from django.apps import AppConfig\n\nclass M03ArtStudioConfig(AppConfig):\n    name = 'M03_art_studio'\n",
    f"{BASE_DIR}/urls.py": "from django.urls import path\nfrom .views import studio, preview, api\n\nurlpatterns = []\n",

    # MODELS
    f"{BASE_DIR}/models/__init__.py": "",
    f"{BASE_DIR}/models/template.py": "",
    f"{BASE_DIR}/models/object.py": "",
    f"{BASE_DIR}/models/params.py": "",
    f"{BASE_DIR}/models/object_type.py": "",
    f"{BASE_DIR}/models/template_type.py": "",

    # SERVICES
    f"{BASE_DIR}/services/__init__.py": "",
    f"{BASE_DIR}/services/renderer.py": "",
    f"{BASE_DIR}/services/validators.py": "",
    f"{BASE_DIR}/services/registry.py": "",

    # UTILS
    f"{BASE_DIR}/utils/__init__.py": "",
    f"{BASE_DIR}/utils/svg_shapes.py": "",
    f"{BASE_DIR}/utils/color_utils.py": "",
    f"{BASE_DIR}/utils/template_logic.py": "",

    # FACTORIES
    f"{BASE_DIR}/factories/__init__.py": "",
    f"{BASE_DIR}/factories/template_factory.py": "",
    f"{BASE_DIR}/factories/object_factory.py": "",

    # VIEWS
    f"{BASE_DIR}/views/__init__.py": "",
    f"{BASE_DIR}/views/studio.py": "",
    f"{BASE_DIR}/views/preview.py": "",
    f"{BASE_DIR}/views/api.py": "",
}

# HTML dosyaları
HTML_FILES = {
    f"{BASE_DIR}/templates/M03_art_studio/base_studio.html": "",
    f"{BASE_DIR}/templates/M03_art_studio/preview_panel.html": "",
    f"{BASE_DIR}/templates/M03_art_studio/template_list.html": "",
    f"{BASE_DIR}/templates/M03_art_studio/template_edit.html": "",
    f"{BASE_DIR}/templates/M03_art_studio/object_preview.html": "",
}

# CSS dosyaları
CSS_FILES = {
    f"{BASE_DIR}/static/M03_art_studio/css/studio.css": "",
    f"{BASE_DIR}/static/M03_art_studio/css/preview.css": "",
}

# JS dosyaları
JS_FILES = {
    f"{BASE_DIR}/static/M03_art_studio/js/studio.js": "",
    f"{BASE_DIR}/static/M03_art_studio/js/preview.js": "",
}


def create_dirs():
    for d in DIRS:
        os.makedirs(d, exist_ok=True)
        print(f"[DIR] {d}")


def create_files(files_dict):
    for path, content in files_dict.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[FILE] {path}")


def main():
    print("\n=== M03_art_studio modülü oluşturuluyor ===\n")
    create_dirs()
    create_files(PY_FILES)
    create_files(HTML_FILES)
    create_files(CSS_FILES)
    create_files(JS_FILES)
    print("\n=== TAMAMLANDI! Art Studio modülü oluşturuldu. ===\n")


if __name__ == "__main__":
    main()
