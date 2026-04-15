# app.py
from ui.stylesheets.utils import inject_css
import streamlit as st


inject_css()


# ----------------------------
# STYLES
# ----------------------------
from ui.stylesheets.utils import inject_css

# ----------------------------
# LAYOUT
# ----------------------------
from ui.layouts.app_shell import app_shell

# ----------------------------
# SECTIONS
# ----------------------------
from ui.sections.upload_section import render_upload_section
from ui.sections.voice_library_section import render_voice_library_section
from ui.sections.generation_section import render_generation_section
from ui.sections.preview_section import render_preview_section

# ----------------------------
# HELPERS
# ----------------------------
from ui.helpers.ui_state import init_ui_state
from ui.helpers.constants import ROUTES


# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="Voice AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# INIT (VERY IMPORTANT)
# =========================================================
inject_css()
init_ui_state()


# =========================================================
# ROUTER (CORE LOGIC)
# =========================================================
def render_route():
    route = st.session_state.get("route")

    # ----------------------------
    # HOME
    # ----------------------------
    if route == ROUTES.HOME:
        st.markdown("## 👋 Welcome")
        st.markdown("Generate ultra-realistic voices with AI")

    # ----------------------------
    # GENERATE FLOW
    # ----------------------------
    elif route == ROUTES.GENERATE:
        render_upload_section()
        render_generation_section()
        render_preview_section()

    # ----------------------------
    # VOICE LIBRARY
    # ----------------------------
    elif route == ROUTES.VOICES:
        render_voice_library_section()

    # ----------------------------
    # FALLBACK
    # ----------------------------
    else:
        st.error("Invalid route")


# =========================================================
# APP RENDER (ENTRY POINT)
# =========================================================
app_shell(render_route)