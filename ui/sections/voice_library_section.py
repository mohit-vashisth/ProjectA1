# voice_library_section.py
import streamlit as st

# ----------------------------------------
# MOCK DATA (replace later with API)
# ----------------------------------------
VOICES = [
    {
        "id": "v1",
        "name": "Aarav",
        "desc": "Warm Indian male voice",
        "tag": "Cloned",
    },
    {
        "id": "v2",
        "name": "Emma",
        "desc": "Soft female narration voice",
        "tag": "Default",
    },
    {
        "id": "v3",
        "name": "Raj",
        "desc": "Deep podcast-style voice",
        "tag": "Cloned",
    },
    {
        "id": "v4",
        "name": "Sophia",
        "desc": "Clear AI assistant voice",
        "tag": "Default",
    },
]


# ----------------------------------------
# MAIN RENDER FUNCTION
# ----------------------------------------
def render_voice_library_section():

    st.markdown("## 🎙️ Voice Library")

    # -------------------------
    # SEARCH + FILTER BAR
    # -------------------------
    col1, col2 = st.columns([3, 1])

    with col1:
        search = st.text_input("Search voices...", key="voice_search")

    with col2:
        filter_type = st.selectbox(
            "Filter",
            ["All", "Cloned", "Default"],
            key="voice_filter"
        )

    # -------------------------
    # FILTER LOGIC
    # -------------------------
    filtered = []

    for v in VOICES:

        if search and search.lower() not in v["name"].lower():
            continue

        if filter_type != "All" and v["tag"] != filter_type:
            continue

        filtered.append(v)

    # -------------------------
    # EMPTY STATE
    # -------------------------
    if not filtered:
        st.info("No voices found.")
        return

    # -------------------------
    # GRID LAYOUT
    # -------------------------
    cols = st.columns(2)

    for i, voice in enumerate(filtered):

        with cols[i % 2]:

            render_voice_card(voice)


# ----------------------------------------
# VOICE CARD COMPONENT (LOCAL)
# ----------------------------------------
def render_voice_card(voice):

    st.markdown(f"""
    <div class="custom-card">
        <div class="card-title">{voice['name']}</div>
        <div class="card-subtitle">{voice['desc']}</div>
        <div class="card-badge">{voice['tag']}</div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------
    # ACTION BUTTONS
    # -------------------------
    col1, col2 = st.columns(2)

    with col1:
        if st.button("▶ Preview", key=f"preview_{voice['id']}"):
            st.info(f"Playing preview for {voice['name']}")

    with col2:
        if st.button("Select", key=f"select_{voice['id']}"):
            st.session_state["selected_voice"] = voice
            st.success(f"Selected: {voice['name']}")