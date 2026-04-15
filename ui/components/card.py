# card.py
import streamlit as st


def card(
    title=None,
    subtitle=None,
    description=None,
    icon=None,
    badge=None,
    footer=None,
    on_click=None,
    key=None,
):
    """
    Generic reusable card component
    Uses global CSS from utils.py
    """

    container = st.container()

    with container:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)

        # ---------------------------
        # BADGE
        # ---------------------------
        if badge:
            st.markdown(
                f'<span class="card-badge">{badge}</span>',
                unsafe_allow_html=True
            )

        # ---------------------------
        # TITLE + ICON
        # ---------------------------
        if icon or title:
            st.markdown(
                f'<div class="card-title">{icon or ""} {title or ""}</div>',
                unsafe_allow_html=True
            )

        # ---------------------------
        # SUBTITLE
        # ---------------------------
        if subtitle:
            st.markdown(
                f'<div class="card-subtitle">{subtitle}</div>',
                unsafe_allow_html=True
            )

        # ---------------------------
        # DESCRIPTION
        # ---------------------------
        if description:
            st.markdown(
                f'<div class="card-desc">{description}</div>',
                unsafe_allow_html=True
            )

        # ---------------------------
        # FOOTER (actions)
        # ---------------------------
        if footer:
            footer()

        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------
    # CLICK HANDLING
    # ---------------------------
    if on_click:
        if st.button("Select", key=key):
            on_click()