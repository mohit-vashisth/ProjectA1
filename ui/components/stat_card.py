# stat_card.py
from ui.components.card import card

def stat_card(icon, value, label):
    card(
        icon=icon,
        title=value,
        subtitle=label
    )