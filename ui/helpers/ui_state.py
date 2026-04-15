# ui_state.py
import streamlit as st
from typing import Any, Optional


# =========================
# DEFAULT STATE SCHEMA
# =========================

DEFAULT_STATE = {
    "route": "home",

    # Upload
    "uploaded_file": None,

    # Voice selection
    "active_voice_id": None,
    "active_voice_name": None,

    # Generation
    "input_text": "",
    "is_generating": False,

    # Output
    "generated_audio": None,
    "generation_error": None,

    # UI flags
    "show_preview": False,
    "show_loader": False,
}


# =========================
# INIT STATE
# =========================

def init_ui_state():
    """
    Initialize all required session state variables.
    Safe to call multiple times.
    """

    for key, value in DEFAULT_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = value


# =========================
# ROUTING
# =========================

def set_route(route: str):
    """
    Change active route (navigation)
    """
    st.session_state["route"] = route


def get_route() -> str:
    return st.session_state.get("route", "home")


# =========================
# FILE HANDLING
# =========================

def set_uploaded_file(file: Any):
    st.session_state["uploaded_file"] = file


def get_uploaded_file():
    return st.session_state.get("uploaded_file")


def clear_uploaded_file():
    st.session_state["uploaded_file"] = None


# =========================
# VOICE SELECTION
# =========================

def set_active_voice(voice_id: str, voice_name: Optional[str] = None):
    st.session_state["active_voice_id"] = voice_id
    st.session_state["active_voice_name"] = voice_name


def get_active_voice():
    return {
        "id": st.session_state.get("active_voice_id"),
        "name": st.session_state.get("active_voice_name"),
    }


def clear_active_voice():
    st.session_state["active_voice_id"] = None
    st.session_state["active_voice_name"] = None


# =========================
# TEXT INPUT
# =========================

def set_input_text(text: str):
    st.session_state["input_text"] = text


def get_input_text() -> str:
    return st.session_state.get("input_text", "")


def clear_input_text():
    st.session_state["input_text"] = ""


# =========================
# GENERATION STATE
# =========================

def start_generation():
    st.session_state["is_generating"] = True
    st.session_state["generation_error"] = None
    st.session_state["show_loader"] = True


def stop_generation():
    st.session_state["is_generating"] = False
    st.session_state["show_loader"] = False


def set_generation_error(error: str):
    st.session_state["generation_error"] = error
    stop_generation()


def get_generation_status():
    return {
        "is_generating": st.session_state.get("is_generating", False),
        "error": st.session_state.get("generation_error"),
    }


# =========================
# OUTPUT / AUDIO
# =========================

def set_generated_audio(audio: Any):
    st.session_state["generated_audio"] = audio
    st.session_state["show_preview"] = True
    stop_generation()


def get_generated_audio():
    return st.session_state.get("generated_audio")


def clear_generated_audio():
    st.session_state["generated_audio"] = None
    st.session_state["show_preview"] = False


# =========================
# UI FLAGS
# =========================

def show_preview():
    st.session_state["show_preview"] = True


def hide_preview():
    st.session_state["show_preview"] = False


def is_preview_visible() -> bool:
    return st.session_state.get("show_preview", False)


def show_loader():
    st.session_state["show_loader"] = True


def hide_loader():
    st.session_state["show_loader"] = False


def is_loading() -> bool:
    return st.session_state.get("show_loader", False)


# =========================
# RESET (VERY IMPORTANT)
# =========================

def reset_generation_flow():
    """
    Reset everything related to generation
    """
    clear_uploaded_file()
    clear_input_text()
    clear_generated_audio()
    clear_active_voice()

    st.session_state["generation_error"] = None
    st.session_state["is_generating"] = False
    st.session_state["show_loader"] = False
    st.session_state["show_preview"] = False