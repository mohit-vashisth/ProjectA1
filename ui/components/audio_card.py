# audio_card.py
import streamlit as st
from ui.components.card import card

def audio_card(audio_file):

    card(title="Audio Preview")

    st.audio(audio_file)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.button("MP3")
    with col2:
        st.button("WAV")
    with col3:
        st.button("OGG")