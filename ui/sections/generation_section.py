# generation_section.py
import streamlit as st


def render_generation_section():

    st.markdown("## 🎙️ Generate Voice")

    # ----------------------------
    # SESSION STATE INIT
    # ----------------------------
    if "gen_text" not in st.session_state:
        st.session_state.gen_text = ""

    if "selected_voice" not in st.session_state:
        st.session_state.selected_voice = "Default Voice"

    if "language" not in st.session_state:
        st.session_state.language = "English"

    if "speed" not in st.session_state:
        st.session_state.speed = 1.0

    if "pitch" not in st.session_state:
        st.session_state.pitch = 1.0

    if "stability" not in st.session_state:
        st.session_state.stability = 0.5

    # ----------------------------
    # TEXT INPUT
    # ----------------------------
    st.markdown("### ✍️ Script")

    st.session_state.gen_text = st.text_area(
        "Enter text to generate voice",
        value=st.session_state.gen_text,
        height=120,
        placeholder="Type your script here..."
    )

    # ----------------------------
    # VOICE + LANGUAGE
    # ----------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🧠 Voice")

        voices = [
            "Default Voice",
            "Male Deep",
            "Female Soft",
            "Narrator",
        ]

        st.session_state.selected_voice = st.selectbox(
            "Select Voice",
            voices,
            index=voices.index(st.session_state.selected_voice)
        )

    with col2:
        st.markdown("### 🌍 Language")

        languages = [
            "English",
            "Hindi",
            "Spanish",
            "French",
        ]

        st.session_state.language = st.selectbox(
            "Select Language",
            languages,
            index=languages.index(st.session_state.language)
        )

    # ----------------------------
    # ADVANCED CONTROLS
    # ----------------------------
    st.markdown("### ⚙️ Controls")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.session_state.speed = st.slider(
            "Speed",
            min_value=0.5,
            max_value=2.0,
            value=st.session_state.speed,
            step=0.1
        )

    with col2:
        st.session_state.pitch = st.slider(
            "Pitch",
            min_value=0.5,
            max_value=2.0,
            value=st.session_state.pitch,
            step=0.1
        )

    with col3:
        st.session_state.stability = st.slider(
            "Stability",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.stability,
            step=0.05
        )

    # ----------------------------
    # VALIDATION
    # ----------------------------
    error = None

    if not st.session_state.gen_text.strip():
        error = "Please enter some text"

    if "uploaded_file" not in st.session_state:
        error = "Upload a voice sample first"

    if error:
        st.warning(error)

    # ----------------------------
    # GENERATE BUTTON
    # ----------------------------
    generate_clicked = st.button(
        "🚀 Generate Voice",
        use_container_width=True,
        disabled=bool(error)
    )

    # ----------------------------
    # GENERATE ACTION
    # ----------------------------
    if generate_clicked:

        st.session_state["is_generating"] = True

        with st.spinner("Generating voice..."):

            # 🔥 THIS IS WHERE API WILL COME LATER
            # ------------------------------------
            # from ui.api.voice_api import generate_voice
            #
            # response = generate_voice(
            #     text=st.session_state.gen_text,
            #     voice=st.session_state.selected_voice,
            #     language=st.session_state.language,
            #     speed=st.session_state.speed,
            #     pitch=st.session_state.pitch,
            #     stability=st.session_state.stability,
            #     file=st.session_state.uploaded_file
            # )
            #
            # st.session_state["generated_audio"] = response["audio_url"]

            # TEMP MOCK
            import time
            time.sleep(1.5)

            st.session_state["generated_audio"] = "sample.mp3"
            st.session_state["is_generating"] = False

        st.success("Voice generated successfully!")