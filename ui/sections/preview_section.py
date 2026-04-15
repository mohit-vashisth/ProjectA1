# preview_section.py
import streamlit as st


def render_preview_section():
    """
    Handles:
    - Empty state
    - Loading state
    - Success state
    - Error state
    """

    st.markdown("## 🎧 Preview")

    # ----------------------------
    # STATE FLAGS
    # ----------------------------
    is_loading = st.session_state.get("is_generating", False)
    audio_data = st.session_state.get("generated_audio", None)
    error = st.session_state.get("generation_error", None)

    # ----------------------------
    # EMPTY STATE
    # ----------------------------
    if not is_loading and not audio_data and not error:
        st.markdown(
            """
            <div class="custom-card">
                <div class="card-title">No Audio Generated</div>
                <div class="card-desc">
                    Generate audio to preview it here.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # ----------------------------
    # LOADING STATE
    # ----------------------------
    if is_loading:
        st.markdown(
            """
            <div class="custom-card">
                <div class="card-title">Generating Audio...</div>
                <div class="card-desc">
                    Please wait while we process your request.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(70)  # placeholder progress
        return

    # ----------------------------
    # ERROR STATE
    # ----------------------------
    if error:
        st.markdown(
            f"""
            <div class="custom-card">
                <div class="card-title">❌ Error</div>
                <div class="card-desc">{error}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Retry"):
            st.session_state["generation_error"] = None
            st.rerun()

        return

    # ----------------------------
    # SUCCESS STATE
    # ----------------------------
    st.markdown(
        """
        <div class="custom-card">
            <div class="card-title">Generated Audio</div>
            <div class="card-subtitle">Your voice is ready</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 🎧 AUDIO PLAYER
    st.audio(audio_data, format="audio/mp3")

    # ----------------------------
    # ACTIONS
    # ----------------------------
    col1, col2, col3 = st.columns(3)

    # DOWNLOAD
    with col1:
        st.download_button(
            label="⬇ Download",
            data=audio_data,
            file_name="generated_audio.mp3",
            mime="audio/mpeg",
        )

    # REGENERATE
    with col2:
        if st.button("🔁 Regenerate"):
            st.session_state["generated_audio"] = None
            st.session_state["is_generating"] = False
            st.rerun()

    # CLEAR
    with col3:
        if st.button("🗑 Clear"):
            st.session_state["generated_audio"] = None
            st.rerun()