import streamlit as st
from ui.stylesheets.utils import inject_css

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Voice AI Studio", layout="wide", page_icon="🎙️")

# -----------------------------
# Session State Init
# -----------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "dark"  # default dark
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "generated_audio" not in st.session_state:
    st.session_state.generated_audio = None
if "voices" not in st.session_state:
    st.session_state.voices = [
        {"id": "v1", "name": "Aarav", "tag": "Cloned"},
        {"id": "v2", "name": "Emma", "tag": "Default"},
        {"id": "v3", "name": "Raj", "tag": "Cloned"},
    ]
if "selected_voice_id" not in st.session_state:
    st.session_state.selected_voice_id = None

# -----------------------------
# Inject CSS with current theme
# -----------------------------
inject_css(st.session_state.theme)

# -----------------------------
# Sidebar: Theme Toggle & Info
# -----------------------------
with st.sidebar:
    st.markdown("## 🎛️ Studio Settings")
    theme_option = st.radio(
        "Theme",
        options=["🌙 Dark", "☀️ Light"],
        index=0 if st.session_state.theme == "dark" else 1,
        horizontal=True,
        help="Switch between dark and light mode"
    )
    # Update theme if changed
    new_theme = "dark" if "Dark" in theme_option else "light"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

    st.divider()
    st.markdown("### 📊 Quick Stats")
    st.metric("Total Voices", len(st.session_state.voices))
    st.metric("Generated Clips", "28")
    st.caption("v1.0.0 · Professional Edition")

# -----------------------------
# Main Header
# -----------------------------
st.markdown("""
<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
    <h1 style="margin:0;">🎙️ Voice AI Studio</h1>
    <span style="background: var(--brand-primary); color: white; padding: 4px 12px; border-radius: 20px; font-size: 14px; font-weight: 500;">Free</span>
</div>
<p style="font-size: 18px; color: var(--text-muted); margin-top: 0;">Clone and generate lifelike voices in seconds</p>
""", unsafe_allow_html=True)

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "🎤 Upload", "🎙️ Generate", "📚 Library"])

# =============================
# TAB 1: HOME
# =============================
with tab1:
    # Welcome
    st.markdown("""
    <div style="margin-bottom: 32px;">
        <h2>Welcome back, John 👋</h2>
        <p style="font-size: 16px;">Let's create something amazing with your voice today.</p>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    cols = st.columns(4)
    stats = [
        ("🎤", "12", "Total Clones"),
        ("💾", "45 MB", "Storage Used"),
        ("⭐", "3", "Premium Voices"),
        ("🔊", "28", "Generated Audio"),
    ]
    for col, (icon, value, label) in zip(cols, stats):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">{icon}</div>
                <div>
                    <div class="stat-value">{value}</div>
                    <div class="stat-label">{label}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Quick Actions
    st.markdown('<div class="section-header"><h3>Quick Actions</h3></div>', unsafe_allow_html=True)
    qcols = st.columns(3)
    actions = [
        ("🎤", "New Voice Clone", "Clone your voice with AI", "home_clone"),
        ("✍️", "Generate Speech", "Convert text to audio", "home_generate"),
        ("📚", "Voice Library", "Manage your voices", "home_library"),
    ]
    for col, (icon, title, desc, key) in zip(qcols, actions):
        with col:
            st.markdown(f"""
            <div class="action-card">
                <div class="action-icon">{icon}</div>
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Get Started", key=key, use_container_width=True):
                if "clone" in key:
                    st.info("👉 Go to the **Upload** tab to start cloning.")
                elif "generate" in key:
                    st.info("👉 Go to the **Generate** tab to create speech.")
                else:
                    st.info("👉 Your voice library is in the **Library** tab.")

    # Recent Files
    st.markdown('<div class="section-header"><h3>Recent Files</h3><span class="view-all">View All →</span></div>', unsafe_allow_html=True)
    fcols = st.columns(3)
    recent = [("voice_sample.mp3", "2.3 MB"), ("clone_output.wav", "5.1 MB"), ("meeting_notes.mp3", "3.8 MB")]
    for i, (col, (name, size)) in enumerate(zip(fcols, recent)):
        with col:
            st.markdown(f"""
            <div class="file-card">
                <div class="file-icon">🎵</div>
                <div style="flex:1;">
                    <div class="file-name">{name}</div>
                    <div class="file-meta">{size}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("▶ Play", key=f"recent_play_{i}"):
                st.info(f"Playing {name} (mock preview)")

# =============================
# TAB 2: UPLOAD VOICE SAMPLE
# =============================
with tab2:
    st.markdown("## 🎧 Upload Voice Sample")
    st.write("Upload a clean voice sample (WAV or MP3, max 10MB).")

    uploaded = st.file_uploader("Choose audio file", type=["wav", "mp3"], key="voice_upload")
    if uploaded:
        st.session_state.uploaded_file = uploaded
        st.success(f"Uploaded: {uploaded.name}")
        st.audio(uploaded)

    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("🎤 Clone Voice", key="clone_btn", use_container_width=True):
            if st.session_state.uploaded_file:
                with st.spinner("Cloning voice..."):
                    import time
                    time.sleep(2)
                    new_voice = {
                        "id": f"v{len(st.session_state.voices)+1}",
                        "name": uploaded.name.split('.')[0], # type: ignore
                        "tag": "Cloned"
                    }
                    st.session_state.voices.append(new_voice)
                    st.success(f"Voice '{new_voice['name']}' cloned successfully!")
                    st.balloons()
            else:
                st.error("Please upload a file first.")

# =============================
# TAB 3: GENERATE VOICE
# =============================
with tab3:
    st.markdown("## 🎙️ Generate Voice")

    voice_names = [v["name"] for v in st.session_state.voices]
    if voice_names:
        selected_name = st.selectbox("Select Voice", voice_names)
        selected_voice = next(v for v in st.session_state.voices if v["name"] == selected_name)
        st.session_state.selected_voice_id = selected_voice["id"]
    else:
        st.warning("No voices available. Please clone or add a voice first.")
        selected_voice = None

    text = st.text_area("Enter text to speak", height=150, placeholder="Type your script here...")

    with st.expander("🎛️ Advanced Settings", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            speed = st.slider("Speed", 0.5, 2.0, 1.0, 0.1)
        with col2:
            pitch = st.slider("Pitch", 0.5, 2.0, 1.0, 0.1)
        with col3:
            stability = st.slider("Stability", 0.0, 1.0, 0.5, 0.05)

    if st.button("🚀 Generate Voice", disabled=not (text and selected_voice), use_container_width=True):
        with st.spinner("Generating..."):
            import time
            time.sleep(2)
            st.session_state.generated_audio = b"MOCK_AUDIO_DATA"
            st.success("Voice generated!")

    if st.session_state.generated_audio:
        st.markdown("---")
        st.markdown("### 🎧 Preview")
        st.audio(st.session_state.generated_audio, format="audio/mp3")
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "⬇ Download",
                data=st.session_state.generated_audio,
                file_name="generated.mp3",
                mime="audio/mpeg",
                use_container_width=True
            )
        with col2:
            if st.button("🗑 Clear", use_container_width=True):
                st.session_state.generated_audio = None
                st.rerun()

# =============================
# TAB 4: VOICE LIBRARY
# =============================
with tab4:
    st.markdown("## 📚 Voice Library")

    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("🔍 Search voices...", placeholder="Type a name...")
    with col2:
        filter_type = st.selectbox("Filter", ["All", "Cloned", "Default"])

    filtered = st.session_state.voices
    if search:
        filtered = [v for v in filtered if search.lower() in v["name"].lower()]
    if filter_type != "All":
        filtered = [v for v in filtered if v["tag"] == filter_type]

    if not filtered:
        st.info("No voices found.")
    else:
        cols = st.columns(2)
        for i, voice in enumerate(filtered):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="custom-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span class="card-title">{voice['name']}</span>
                        <span class="card-badge">{voice['tag']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("▶ Preview", key=f"preview_{voice['id']}", use_container_width=True):
                        st.info(f"Preview {voice['name']} (mock)")
                with c2:
                    if st.button("Select", key=f"select_{voice['id']}", use_container_width=True):
                        st.session_state.selected_voice_id = voice["id"]
                        st.success(f"Selected: {voice['name']}")

    st.divider()
    if st.button("➕ Add Sample Voice", use_container_width=True):
        st.session_state.voices.append({
            "id": f"v{len(st.session_state.voices)+1}",
            "name": f"Sample {len(st.session_state.voices)+1}",
            "tag": "Default"
        })
        st.rerun()