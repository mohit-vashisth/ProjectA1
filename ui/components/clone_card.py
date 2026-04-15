# alone_card.py
import streamlit as st
from ui.components.card import card

def clone_card(title, badge, icon, specs, features, on_select):

    def footer():
        if st.button(f"Select {title}", key=title):
            on_select()

    description = "\n".join([f"• {f}" for f in features])

    card(
        title=title,
        subtitle=badge,
        description=description,
        icon=icon,
        footer=footer
    )