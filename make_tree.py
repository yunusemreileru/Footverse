import os

# Hariç tutulacak klasör ve dosyalar
EXCLUDE_DIRS = {
    ".venv", "__pycache__", ".git", ".idea", ".vscode",
    "migrations", "staticfiles", "media", "env", "node_modules"
}

EXCLUDE_FILES = {
    "__init__.pyc", ".DS_Store", "tree.txt", "make_tree.py"
}

OUTPUT_FILE = "tree.txt"


def should_exclude(name):
    return name in EXCLUDE_DIRS or name in EXCLUDE_FILES


def generate_tree(start_path, prefix=""):
    items = sorted(os.listdir(start_path))
    lines = []

    for index, item in enumerate(items):
        if should_exclude(item):
            continue

        full_path = os.path.join(start_path, item)
        connector = "├── " if index < len(items) - 1 else "└── "

        lines.append(prefix + connector + item)

        if os.path.isdir(full_path):
            extension = "│   " if index < len(items) - 1 else "    "
            lines.extend(generate_tree(full_path, prefix + extension))

    return lines


def main():
    base_path = os.getcwd()
    tree_lines = ["Proje Dosya Yapısı:\n"]
    tree_lines.extend(generate_tree(base_path))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(tree_lines))

    print(f"Tree oluşturuldu: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
