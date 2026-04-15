# upload_section.py
import streamlit as st
from ui.components.card import card
from ui.components.input import file_uploader_input


# ----------------------------
# CONFIG
# ----------------------------
SUPPORTED_TYPES = ["wav", "mp3"]
MAX_FILE_SIZE_MB = 10


# ----------------------------
# STATE INIT
# ----------------------------
def _init_state():
    defaults = {
        "uploaded_file": None,
        "uploaded_file_name": None,
        "uploaded_file_type": None,
        "uploaded_file_size": None,
        "upload_error": None,
        "upload_ready": False,
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ----------------------------
# VALIDATION
# ----------------------------
def _validate_file(file):

    if not file:
        return False, "No file uploaded"

    # File size check
    file_size_mb = file.size / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        return False, f"File too large (> {MAX_FILE_SIZE_MB} MB)"

    # File type check
    file_type = file.name.split(".")[-1].lower()
    if file_type not in SUPPORTED_TYPES:
        return False, f"Unsupported format ({file_type})"

    return True, None


# ----------------------------
# STATE UPDATE
# ----------------------------
def _update_state(file, is_valid, error):

    if is_valid:
        st.session_state.uploaded_file = file
        st.session_state.uploaded_file_name = file.name
        st.session_state.uploaded_file_type = file.name.split(".")[-1]
        st.session_state.uploaded_file_size = file.size
        st.session_state.upload_error = None
        st.session_state.upload_ready = True
    else:
        st.session_state.upload_error = error
        st.session_state.upload_ready = False


# ----------------------------
# UI RENDER
# ----------------------------
def render_upload_section():

    _init_state()

    st.markdown("## 🎧 Upload Voice Sample")
    st.write("Upload a clean voice sample (WAV or MP3, max 10MB).")

    # ----------------------------
    # UPLOAD CARD
    # ----------------------------
    def upload_ui():

        file = file_uploader_input(
            label="Upload Audio File",
            key="voice_upload",
            type=SUPPORTED_TYPES
        )

        is_valid, error = _validate_file(file)

        if file:
            _update_state(file, is_valid, error)

        # ----------------------------
        # STATUS DISPLAY
        # ----------------------------
        if st.session_state.upload_error:
            st.error(st.session_state.upload_error)

        elif st.session_state.upload_ready:
            st.success(f"Uploaded: {st.session_state.uploaded_file_name}")

            # Preview audio
            st.audio(st.session_state.uploaded_file)

    # Render inside card
    card(
        title="Voice Upload",
        description="Provide a high-quality voice sample for best results.",
        icon="🎤",
        footer=upload_ui
    )