# voice_card.py
import streamlit as st
from ui.components.card import card

def voice_card(name, type, on_select):

    def footer():
        if st.button("Use", key=name):
            on_select()

    card(
        title=name,
        subtitle=type,
        icon="🎙️",
        footer=footer
    )