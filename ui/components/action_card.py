# action_card.py
import streamlit as st
from ui.components.card import card

def action_card(icon, title, description, on_click):

    def footer():
        if st.button("Open", key=title):
            on_click()

    card(
        icon=icon,
        title=title,
        description=description,
        footer=footer
    )