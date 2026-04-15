# home_section.py
import streamlit as st
from ui.components.card import card
from ui.components.button import primary_button


def render_home_section():

    # =============================
    # HERO SECTION
    # =============================
    st.markdown(
        """
        <div style="margin-bottom: 32px;">
            <h1>🎙️ Voice AI Studio</h1>
            <p>Create ultra-realistic AI voices in seconds.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([3, 1])

    with col1:
        st.write("Generate natural-sounding speech using your own cloned voices.")

    with col2:
        if primary_button("🎙️ Generate Voice", key="go_generate"):
            st.session_state.route = "generate"

    st.markdown("---")

    # =============================
    # QUICK ACTIONS
    # =============================
    st.markdown("### ⚡ Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        card(
            title="Generate Voice",
            subtitle="Text → Speech",
            description="Convert text into realistic voice",
        )
        if st.button("Start", key="qa_generate"):
            st.session_state.route = "generate"

    with col2:
        card(
            title="Upload Voice",
            subtitle="Clone Voice",
            description="Train your own voice model",
        )
        if st.button("Upload", key="qa_upload"):
            st.session_state.route = "generate"

    with col3:
        card(
            title="Voice Library",
            subtitle="Manage Voices",
            description="View and manage saved voices",
        )
        if st.button("Open Library", key="qa_library"):
            st.session_state.route = "voices"

    st.markdown("---")

    # =============================
    # STATS / RECENT
    # =============================
    st.markdown("### 📊 Your Activity")

    col1, col2, col3 = st.columns(3)

    with col1:
        card(
            title="Voices",
            subtitle="Total Created",
            description="12 voices"
        )

    with col2:
        card(
            title="Generations",
            subtitle="Total Usage",
            description="48 generations"
        )

    with col3:
        card(
            title="Credits",
            subtitle="Remaining",
            description="320 credits"
        )

    st.markdown("---")

    # =============================
    # RECENT PROJECTS (PLACEHOLDER)
    # =============================
    st.markdown("### 🧠 Recent Generations")

    for i in range(3):
        card(
            title=f"Sample Audio {i+1}",
            subtitle="Generated voice preview",
            description="Click to play or download"
        )