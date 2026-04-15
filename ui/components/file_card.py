# file_card.py
from ui.components.card import card

def file_card(name, size, file_type):
    card(
        title=name,
        subtitle=f"{file_type} • {size}",
        icon="📄"
    )