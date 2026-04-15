# route.py
import streamlit as st

# Sections import
from ui.sections.upload_section import render_upload_section
from ui.sections.voice_library_section import render_voice_library_section
from ui.sections.generation_section import render_generation_section
from ui.sections.preview_section import render_preview_section


# ----------------------------
# ROUTE CONSTANTS
# ----------------------------
ROUTES = {
    "home": "home",
    "generate": "generate",
    "voices": "voices",
}


# ----------------------------
# ROUTE SETTER
# ----------------------------
def set_route(route: str):
    """
    Update current route in session state
    """
    if route in ROUTES.values():
        st.session_state.route = route
    else:
        st.session_state.route = "home"


# ----------------------------
# ROUTE GETTER
# ----------------------------
def get_route() -> str:
    """
    Safely get current route
    """
    return st.session_state.get("route", "home")


# ----------------------------
# MAIN ROUTER
# ----------------------------
def render_route():
    """
    Main routing function
    Decides which UI to render
    """

    route = get_route()

    # ----------------------------
    # HOME
    # ----------------------------
    if route == "home":
        render_home()

    # ----------------------------
    # GENERATE PAGE
    # ----------------------------
    elif route == "generate":
        render_generate()

    # ----------------------------
    # VOICES PAGE
    # ----------------------------
    elif route == "voices":
        render_voices()

    # ----------------------------
    # FALLBACK
    # ----------------------------
    else:
        render_404()


# ----------------------------
# PAGE DEFINITIONS
# ----------------------------
def render_home():
    st.title("Home")
    st.write("Welcome to Voice AI Platform")


def render_generate():
    """
    Compose multiple sections into one page
    """
    render_upload_section()
    render_generation_section()
    render_preview_section()


def render_voices():
    render_voice_library_section()


def render_404():
    st.error("Page not found")