# audio_player.py
import streamlit as st

def audio_player(audio_bytes=None, audio_url=None):
    """
    Basic audio playback component

    Args:
        audio_bytes: raw audio file
        audio_url: hosted audio URL
    """

    if audio_bytes:
        st.audio(audio_bytes)

    elif audio_url:
        st.audio(audio_url)

    else:
        st.info("No audio available")

def play_pause_button(key: str):
    """
    Toggle play/pause state

    Returns:
        bool → True if playing
    """

    if f"{key}_playing" not in st.session_state:
        st.session_state[f"{key}_playing"] = False

    is_playing = st.session_state[f"{key}_playing"]

    label = "⏸ Pause" if is_playing else "▶ Play"

    if st.button(label, key=f"{key}_btn"):
        st.session_state[f"{key}_playing"] = not is_playing

    return st.session_state[f"{key}_playing"]

def waveform_placeholder():
    """
    Placeholder for waveform visualization
    (to be replaced with real waveform later)
    """

    st.markdown(
        """
        <div style="
            height: 60px;
            background: linear-gradient(90deg, #444, #888);
            border-radius: 8px;
            opacity: 0.6;
        ">
        </div>
        """,
        unsafe_allow_html=True
    )

# ===========================
# Main component
# ===========================
def audio_preview_card(
    title: str,
    audio_bytes=None,
    audio_url=None,
    key: str = "audio",
    show_waveform: bool = True
):
    """
    Full audio preview UI (used in product)

    Args:
        title: card title
        audio_bytes / audio_url: audio source
        key: unique identifier
        show_waveform: toggle waveform
    """

    st.markdown("### " + title)

    with st.container():

        # Waveform (optional)
        if show_waveform:
            waveform_placeholder()

        # Controls
        col1, col2 = st.columns([1, 4])

        with col1:
            is_playing = play_pause_button(key)

        with col2:
            if is_playing:
                audio_player(audio_bytes, audio_url)

        st.markdown("---")