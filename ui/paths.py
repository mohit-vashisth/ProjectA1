from pathlib import Path
from typing import Dict


# ==============================
# CONFIG
# ==============================

IGNORE_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    ".idea",
    ".vscode"
}


# ==============================
# ROOT FIX (IMPORTANT)
# ==============================

# This ensures it ONLY scans the folder where paths.py exists
BASE_DIR = Path(__file__).resolve().parent


# ==============================
# TREE BUILDER
# ==============================

def build_tree(root: Path) -> Dict:
    tree = {}

    for item in sorted(root.iterdir(), key=lambda x: (x.is_file(), x.name.lower())):
        if item.name in IGNORE_DIRS:
            continue

        if item.is_dir():
            tree[item.name] = build_tree(item)
        else:
            tree[item.name] = None

    return tree


# ==============================
# TREE PRINTER
# ==============================

def print_tree(tree: Dict, indent: str = ""):
    items = list(tree.items())

    for i, (name, subtree) in enumerate(items):
        is_last = i == len(items) - 1

        branch = "└── " if is_last else "├── "
        print(indent + branch + name)

        if isinstance(subtree, dict):
            extension = "    " if is_last else "│   "
            print_tree(subtree, indent + extension)


# ==============================
# MAIN FUNCTION
# ==============================

def show_structure():
    print(f"\n📁 Project Folder: {BASE_DIR.name}\n")

    tree = build_tree(BASE_DIR)
    print_tree(tree)


# ==============================
# RUN
# ==============================

if __name__ == "__main__":
    show_structure()