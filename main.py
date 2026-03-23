import streamlit as st
import pandas as pd
import time
import random
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="ProjectA1 - Voice Cloning Platform",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------- Custom CSS (from original style.css, adapted for Streamlit) -------------------
st.markdown("""
<style>
    /* Import font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Override Streamlit defaults */
    .stApp {
        background-color: #0f172a;
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar */
    .css-1d391kg {
        background-color: #1e293b;
        border-right: 1px solid #475569;
    }
    .css-1d391kg .st-emotion-cache-1wrcr25 {
        color: #f1f5f9;
    }
    .sidebar .sidebar-content {
        background-color: #1e293b;
    }
    .st-emotion-cache-1wrcr25 {
        color: #94a3b8;
    }
    .st-emotion-cache-1wrcr25:hover {
        color: #f1f5f9;
        background-color: #334155;
    }
    .st-emotion-cache-1wrcr25.active {
        background-color: rgba(99, 102, 241, 0.1);
        color: #818cf8;
        border-left: 3px solid #6366f1;
    }

    /* Main content area */
    .main-header {
        background-color: #1e293b;
        border-bottom: 1px solid #475569;
        padding: 1rem 2rem;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: #f1f5f9;
        font-size: 1.875rem;
        font-weight: 600;
        margin: 0;
    }

    /* Cards */
    .stat-card {
        background-color: #1e293b;
        border: 1px solid #475569;
        border-radius: 0.75rem;
        padding: 1.25rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: all 0.2s;
    }
    .stat-card:hover {
        border-color: #6366f1;
        transform: translateY(-2px);
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.1);
    }
    .stat-icon {
        width: 56px;
        height: 56px;
        border-radius: 0.75rem;
        background-color: rgba(99, 102, 241, 0.08);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
    }
    .stat-value {
        font-size: 1.875rem;
        font-weight: 700;
        color: #f1f5f9;
        line-height: 1;
    }
    .stat-label {
        font-size: 0.875rem;
        color: #94a3b8;
        margin-top: 0.25rem;
    }

    .action-card {
        background-color: #1e293b;
        border: 1px solid #475569;
        border-radius: 0.75rem;
        padding: 1.5rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s;
    }
    .action-card:hover {
        border-color: #6366f1;
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.15);
    }
    .action-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .action-card h4 {
        color: #f1f5f9;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .action-card p {
        color: #94a3b8;
        font-size: 0.875rem;
    }

    .file-card {
        background-color: #1e293b;
        border: 1px solid #475569;
        border-radius: 0.75rem;
        padding: 1rem;
        transition: all 0.2s;
    }
    .file-card:hover {
        border-color: #6366f1;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    .file-icon {
        width: 48px;
        height: 48px;
        background-color: #334155;
        border-radius: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 0.75rem;
    }
    .file-name {
        font-weight: 500;
        color: #f1f5f9;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .file-info {
        display: flex;
        justify-content: space-between;
        font-size: 0.75rem;
        color: #94a3b8;
        margin: 0.5rem 0;
    }
    .file-actions {
        display: flex;
        gap: 0.5rem;
        margin-top: 0.75rem;
    }
    .file-action-btn {
        flex: 1;
        background-color: #334155;
        border: none;
        border-radius: 0.375rem;
        padding: 0.5rem;
        color: #94a3b8;
        font-size: 0.75rem;
        cursor: pointer;
        transition: all 0.2s;
    }
    .file-action-btn:hover {
        background-color: #6366f1;
        color: white;
    }

    /* TTS */
    .tts-container {
        display: flex;
        gap: 1.5rem;
    }
    .tts-input-section, .tts-preview-section {
        flex: 1;
    }
    .card {
        background-color: #1e293b;
        border: 1px solid #475569;
        border-radius: 0.75rem;
        overflow: hidden;
    }
    .card-header {
        padding: 1rem 1.25rem;
        border-bottom: 1px solid #475569;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .card-header h3 {
        color: #f1f5f9;
        font-weight: 600;
        margin: 0;
    }
    .tts-textarea {
        width: 100%;
        min-height: 200px;
        background-color: #0f172a;
        border: none;
        padding: 1rem;
        color: #f1f5f9;
        font-family: monospace;
        resize: vertical;
    }
    .control-group {
        margin-bottom: 1rem;
    }
    .form-label {
        display: block;
        margin-bottom: 0.5rem;
        font-size: 0.875rem;
        color: #94a3b8;
    }
    .stSelectbox, .stTextInput, .stTextArea {
        background-color: #334155;
        border-color: #475569;
        color: #f1f5f9;
    }

    /* Buttons */
    .btn-primary {
        background-color: #6366f1;
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
        width: 100%;
    }
    .btn-primary:hover {
        background-color: #4f46e5;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    .btn-secondary {
        background-color: #334155;
        border: 1px solid #475569;
        color: #f1f5f9;
    }

    /* Chat */
    .chat-messages {
        height: 400px;
        overflow-y: auto;
        background-color: #0f172a;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    .chat-message {
        margin-bottom: 1rem;
        display: flex;
        gap: 0.75rem;
    }
    .chat-message.user {
        justify-content: flex-end;
    }
    .message-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background-color: #6366f1;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.875rem;
        font-weight: 600;
        color: white;
    }
    .message-content {
        background-color: #1e293b;
        padding: 0.75rem 1rem;
        border-radius: 0.75rem;
        max-width: 70%;
        color: #f1f5f9;
    }
    .chat-message.user .message-content {
        background-color: #6366f1;
    }
    .chat-input {
        display: flex;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    .chat-input input {
        flex: 1;
        padding: 0.75rem;
        border-radius: 0.5rem;
        border: 1px solid #475569;
        background-color: #334155;
        color: #f1f5f9;
    }
    .send-btn {
        background-color: #6366f1;
        border: none;
        border-radius: 0.5rem;
        padding: 0 1rem;
        color: white;
        cursor: pointer;
    }

    /* Voice library */
    .voice-card {
        background-color: #1e293b;
        border: 1px solid #475569;
        border-radius: 0.75rem;
        padding: 1rem;
        transition: all 0.2s;
    }
    .voice-card:hover {
        border-color: #6366f1;
    }
    .voice-card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 0.5rem;
    }
    .voice-type-badge {
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    .voice-type-badge.instant {
        background-color: rgba(34, 197, 94, 0.2);
        color: #4ade80;
    }
    .voice-type-badge.premium {
        background-color: #6366f1;
        color: white;
    }
    .voice-meta {
        font-size: 0.875rem;
        color: #94a3b8;
        margin: 0.5rem 0;
    }
    .voice-card-footer {
        display: flex;
        gap: 0.5rem;
        margin-top: 0.75rem;
    }
    .voice-action-btn {
        flex: 1;
        background-color: #334155;
        border: none;
        border-radius: 0.375rem;
        padding: 0.5rem;
        color: #94a3b8;
        font-size: 0.75rem;
        cursor: pointer;
    }
    .voice-action-btn:hover {
        background-color: #6366f1;
        color: white;
    }

    /* Settings and profile */
    .settings-section {
        background-color: #1e293b;
        border: 1px solid #475569;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .settings-toggle {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 0;
        border-bottom: 1px solid #475569;
    }
    .profile-avatar {
        width: 96px;
        height: 96px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366f1, #818cf8);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        font-weight: bold;
        color: white;
        margin: 0 auto 1rem;
    }
    .progress-bar {
        width: 100%;
        height: 8px;
        background-color: #334155;
        border-radius: 4px;
        overflow: hidden;
        margin: 1rem 0;
    }
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #6366f1, #818cf8);
        width: 0%;
        transition: width 0.3s;
    }
    .toast {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #1e293b;
        border: 1px solid #475569;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        color: #f1f5f9;
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

# ------------------- Initialize Session State -------------------
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dashboard'
if 'files' not in st.session_state:
    st.session_state.files = [
        {'name': 'voice_sample_01.mp3', 'size': '2.4 MB', 'date': '2025-10-28', 'type': 'audio/mp3'},
        {'name': 'presentation_audio.wav', 'size': '5.1 MB', 'date': '2025-10-27', 'type': 'audio/wav'},
        {'name': 'podcast_episode_final.m4a', 'size': '8.7 MB', 'date': '2025-10-26', 'type': 'audio/m4a'},
        {'name': 'demo_voice.mp3', 'size': '1.8 MB', 'date': '2025-10-25', 'type': 'audio/mp3'}
    ]
if 'voices' not in st.session_state:
    st.session_state.voices = [
        {'id': 1, 'name': 'Natural Male', 'type': 'instant', 'language': 'English', 'style': 'Professional'},
        {'id': 2, 'name': 'Natural Female', 'type': 'instant', 'language': 'English', 'style': 'Friendly'},
        {'id': 3, 'name': 'Premium Voice 1', 'type': 'premium', 'language': 'English', 'style': 'Formal'},
        {'id': 4, 'name': 'Casual Voice', 'type': 'instant', 'language': 'English', 'style': 'Natural'}
    ]
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = [
        {'role': 'assistant', 'content': 'Welcome to Voice Cloning Studio! How can I help you today?'},
        {'role': 'user', 'content': 'I want to clone my voice'},
        {'role': 'assistant', 'content': 'Great! You can choose between Instant Clone or Premium Clone. Which would you prefer?'}
    ]
if 'selected_clone_type' not in st.session_state:
    st.session_state.selected_clone_type = None
if 'tts_generated' not in st.session_state:
    st.session_state.tts_generated = False
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'progress' not in st.session_state:
    st.session_state.progress = 0

# ------------------- Helper Functions -------------------
def show_toast(message):
    st.toast(message)

def navigate_to(page):
    st.session_state.current_page = page
    st.rerun()

def get_file_icon(file_type):
    if 'mp3' in file_type:
        return '🎵'
    elif 'wav' in file_type:
        return '🎼'
    elif 'm4a' in file_type:
        return '🍎'
    else:
        return '📄'

def render_recent_files():
    cols = st.columns(4)
    for idx, file in enumerate(st.session_state.files[:4]):
        with cols[idx]:
            st.markdown(f"""
            <div class="file-card">
                <div class="file-icon">{get_file_icon(file['type'])}</div>
                <div class="file-name">{file['name']}</div>
                <div class="file-info">
                    <span>{file['size']}</span>
                    <span>{file['date']}</span>
                </div>
                <div class="file-actions">
                    <button class="file-action-btn" onclick="alert('Playing {file['name']}')">▶️</button>
                    <button class="file-action-btn" onclick="alert('Downloading {file['name']}')">⬇️</button>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ------------------- Sidebar Navigation -------------------
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 2rem;">
        <span style="font-size: 2rem;">🎙️</span>
        <span style="font-size: 1.25rem; font-weight: 600; color: #f1f5f9;">ProjectA1</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Main")
    if st.button("🏠 Dashboard", use_container_width=True):
        navigate_to('dashboard')
    if st.button("🎤 Voice Cloning", use_container_width=True):
        navigate_to('voice_cloning')
    if st.button("✍️ Text-to-Speech", use_container_width=True):
        navigate_to('text_to_speech')
    if st.button("📚 Voice Library", use_container_width=True):
        navigate_to('voice_library')

    st.markdown("### Tools")
    if st.button("📁 File Storage", use_container_width=True):
        navigate_to('file_storage')
    if st.button("💬 Chat Assistant", use_container_width=True):
        navigate_to('chat')
    if st.button("⚙️ Settings", use_container_width=True):
        navigate_to('settings')

    st.markdown("### Account")
    if st.button("👤 Profile", use_container_width=True):
        navigate_to('profile')

    # Storage widget
    st.markdown("---")
    used = 45
    total = 1024  # 1 GB in MB
    percent = (used / total) * 100
    st.markdown(f"""
    <div style="background-color: #334155; padding: 1rem; border-radius: 0.75rem;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="font-size: 0.875rem;">Storage Used</span>
            <span style="font-size: 0.875rem; font-weight: 600; color: #6366f1;">{used} MB / {total} MB</span>
        </div>
        <div style="width: 100%; height: 4px; background-color: #0f172a; border-radius: 2px; overflow: hidden;">
            <div style="width: {percent}%; height: 100%; background: linear-gradient(90deg, #6366f1, #818cf8);"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ------------------- Main Header -------------------
st.markdown(f"""
<div class="main-header">
    <h1>{st.session_state.current_page.replace('_', ' ').title()}</h1>
</div>
""", unsafe_allow_html=True)

# ------------------- Page Content -------------------
current = st.session_state.current_page

# ----- Dashboard -----
if current == 'dashboard':
    # Welcome
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h2 style="color: #f1f5f9; font-weight: 600;">Welcome back, Mohit! 👋</h2>
        <p style="color: #94a3b8;">Let's create something amazing with your voice today.</p>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    col1, col2, col3, col4 = st.columns(4)
    stats = [
        ("🎤", "12", "Total Clones"),
        ("💾", "45 MB", "Storage Used"),
        ("⭐", "3", "Premium Voices"),
        ("🔊", "28", "Generated Audio")
    ]
    for i, (icon, value, label) in enumerate(stats):
        with [col1, col2, col3, col4][i]:
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
    st.markdown("<h3 style='margin: 2rem 0 1rem 0;'>Quick Actions</h3>", unsafe_allow_html=True)
    cols = st.columns(3)
    actions = [
        ("🎤", "New Voice Clone", "Clone your voice with AI technology", "voice_cloning"),
        ("✍️", "Generate Speech", "Convert text to natural-sounding audio", "text_to_speech"),
        ("📚", "Voice Library", "Browse and manage your voices", "voice_library")
    ]
    for i, (icon, title, desc, page) in enumerate(actions):
        with cols[i]:
            if st.button(f"{icon} {title}", use_container_width=True):
                navigate_to(page)
            st.caption(desc)

    # Recent Files
    st.markdown("<h3 style='margin: 2rem 0 1rem 0;'>Recent Files</h3>", unsafe_allow_html=True)
    render_recent_files()
    if st.button("View All", key="view_all_files"):
        navigate_to('file_storage')

# ----- Voice Cloning -----
elif current == 'voice_cloning':
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="card" style="padding: 1.5rem;">
            <div style="position: relative;">
                <span style="position: absolute; top: 0; right: 0; background: #4ade80; color: #0f172a; padding: 0.25rem 0.75rem; border-radius: 100px; font-size: 0.75rem;">Free</span>
                <div style="font-size: 4rem; margin-bottom: 1rem;">⚡</div>
                <h3 style="color: #f1f5f9;">Instant Clone</h3>
                <p style="color: #94a3b8;">Quick & Easy</p>
                <div style="background: #334155; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;">
                    <div>Duration: 5-10 minutes</div>
                    <div>Sample Required: 30 seconds</div>
                    <div>Quality: Good</div>
                </div>
                <ul style="color: #94a3b8; margin-bottom: 1.5rem;">
                    <li>✓ Quick processing</li>
                    <li>✓ Basic voice replication</li>
                    <li>✓ Standard quality output</li>
                    <li>✓ Suitable for demos</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Select Instant Clone", key="instant_btn", use_container_width=True):
            st.session_state.selected_clone_type = 'instant'
            show_toast("Instant Clone selected!")

    with col2:
        st.markdown("""
        <div class="card" style="padding: 1.5rem; border: 2px solid #6366f1;">
            <div style="position: relative;">
                <span style="position: absolute; top: 0; right: 0; background: #6366f1; color: white; padding: 0.25rem 0.75rem; border-radius: 100px; font-size: 0.75rem;">$29/month</span>
                <div style="font-size: 4rem; margin-bottom: 1rem;">💎</div>
                <h3 style="color: #f1f5f9;">Premium Clone</h3>
                <p style="color: #94a3b8;">Professional Quality</p>
                <div style="background: #334155; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;">
                    <div>Duration: 2-4 hours</div>
                    <div>Sample Required: 10 minutes</div>
                    <div>Quality: Excellent</div>
                </div>
                <ul style="color: #94a3b8; margin-bottom: 1.5rem;">
                    <li>✓ High-fidelity cloning</li>
                    <li>✓ Advanced emotion control</li>
                    <li>✓ Professional quality</li>
                    <li>✓ Commercial use license</li>
                    <li>✓ Priority processing</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Select Premium Clone", key="premium_btn", use_container_width=True):
            st.session_state.selected_clone_type = 'premium'
            show_toast("Premium Clone selected!")

    if st.session_state.selected_clone_type:
        st.markdown("---")
        st.subheader("Upload Voice Sample")
        min_dur = "30 seconds" if st.session_state.selected_clone_type == 'instant' else "10 minutes"
        st.caption(f"Minimum duration: {min_dur}")
        uploaded_file = st.file_uploader("Drag & drop or click to browse", type=['mp3', 'wav', 'm4a'])
        if uploaded_file is not None:
            st.info(f"Uploaded: {uploaded_file.name}")
            if st.button("Start Cloning"):
                with st.spinner("Processing your voice..."):
                    progress_bar = st.progress(0)
                    for i in range(101):
                        time.sleep(0.03)
                        progress_bar.progress(i)
                    st.success("Voice cloning completed successfully!")
                    # Add to files
                    new_file = {
                        'name': uploaded_file.name,
                        'size': f"{uploaded_file.size / (1024*1024):.1f} MB",
                        'date': datetime.now().strftime("%Y-%m-%d"),
                        'type': uploaded_file.type
                    }
                    st.session_state.files.insert(0, new_file)
                    st.session_state.selected_clone_type = None
                    st.rerun()

# ----- Text-to-Speech -----
elif current == 'text_to_speech':
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header"><h3>Enter Your Text</h3><span class="char-count">0 / 5000</span></div>', unsafe_allow_html=True)
        text = st.text_area("", height=200, placeholder="Type or paste your text here...", max_chars=5000, key="tts_text")
        char_count = len(text)
        st.markdown(f'<div style="text-align: right; font-size: 0.75rem; color: #94a3b8;">{char_count} / 5000</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="tts-controls">', unsafe_allow_html=True)
        voice = st.selectbox("Select Voice", ["Natural Male - Professional", "Natural Female - Friendly", "Premium Voice 1 - Formal", "Casual Voice - Natural"])
        lang = st.selectbox("Language", ["English", "Spanish", "French", "German", "Italian", "Portuguese", "Japanese", "Chinese", "Hindi", "Arabic"])
        style = st.selectbox("Voice Style", ["Natural", "Professional", "Friendly", "Formal", "Casual", "Energetic"])
        generate = st.button("🔊 Generate Speech", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if generate and text.strip():
            with st.spinner("Generating speech..."):
                time.sleep(2)
                st.session_state.tts_generated = True
                show_toast("Speech generated successfully!")
                st.rerun()

    with col2:
        if st.session_state.tts_generated:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header"><h3>Audio Preview</h3></div>', unsafe_allow_html=True)
            # Dummy waveform visualization
            st.markdown("""
            <div style="display: flex; align-items: center; justify-content: space-between; height: 80px; gap: 2px; margin: 1rem;">
                <div style="flex:1; height: 40%; background-color: #6366f1; border-radius: 2px;"></div>
                <div style="flex:1; height: 70%; background-color: #6366f1; border-radius: 2px;"></div>
                <div style="flex:1; height: 50%; background-color: #6366f1; border-radius: 2px;"></div>
                <div style="flex:1; height: 85%; background-color: #6366f1; border-radius: 2px;"></div>
                <div style="flex:1; height: 60%; background-color: #6366f1; border-radius: 2px;"></div>
                <div style="flex:1; height: 90%; background-color: #6366f1; border-radius: 2px;"></div>
                <div style="flex:1; height: 45%; background-color: #6366f1; border-radius: 2px;"></div>
                <div style="flex:1; height: 75%; background-color: #6366f1; border-radius: 2px;"></div>
            </div>
            """, unsafe_allow_html=True)
            # Simulate audio player
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
            st.markdown("### Export Audio")
            exp_cols = st.columns(4)
            for i, fmt in enumerate(["MP3", "WAV", "OGG", "M4A"]):
                if exp_cols[i].button(f"🎵 {fmt}"):
                    show_toast(f"Exporting as {fmt}...")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Enter text and click Generate to preview audio.")

# ----- Voice Library -----
elif current == 'voice_library':
    # Search and filter
    search = st.text_input("Search voices...", placeholder="Type voice name...")
    filter_type = st.radio("Filter", ["All", "Instant", "Premium"], horizontal=True)

    filtered = st.session_state.voices
    if search:
        filtered = [v for v in filtered if search.lower() in v['name'].lower()]
    if filter_type != "All":
        filtered = [v for v in filtered if v['type'] == filter_type.lower()]

    cols = st.columns(2)
    for idx, voice in enumerate(filtered):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="voice-card">
                <div class="voice-card-header">
                    <div><h4 style="color: #f1f5f9;">{voice['name']}</h4></div>
                    <span class="voice-type-badge {voice['type']}">{voice['type']}</span>
                </div>
                <div class="voice-meta">
                    🌍 {voice['language']}<br>
                    🎭 {voice['style']}
                </div>
                <div class="voice-card-footer">
                    <button class="voice-action-btn" onclick="alert('Previewing {voice['name']}')">▶️ Preview</button>
                    <button class="voice-action-btn" onclick="alert('Selected {voice['name']}')">✓ Select</button>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ----- File Storage -----
elif current == 'file_storage':
    view = st.radio("View", ["Grid", "List"], horizontal=True)
    if view == "Grid":
        cols = st.columns(3)
        for idx, file in enumerate(st.session_state.files):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="file-card">
                    <div class="file-icon">{get_file_icon(file['type'])}</div>
                    <div class="file-name">{file['name']}</div>
                    <div class="file-info">
                        <span>{file['size']}</span>
                        <span>{file['date']}</span>
                    </div>
                    <div class="file-actions">
                        <button class="file-action-btn" onclick="alert('Playing {file['name']}')">▶️</button>
                        <button class="file-action-btn" onclick="alert('Downloading {file['name']}')">⬇️</button>
                        <button class="file-action-btn" onclick="alert('Delete {file['name']}')">🗑️</button>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        for file in st.session_state.files:
            col1, col2, col3, col4 = st.columns([3,1,1,1])
            with col1:
                st.write(f"{get_file_icon(file['type'])} {file['name']}")
            with col2:
                st.write(file['size'])
            with col3:
                st.write(file['date'])
            with col4:
                if st.button("🗑️", key=f"del_{file['name']}"):
                    st.session_state.files = [f for f in st.session_state.files if f['name'] != file['name']]
                    st.rerun()

    uploaded = st.file_uploader("Upload new file", type=['mp3', 'wav', 'm4a', 'txt', 'pdf'])
    if uploaded:
        new_file = {
            'name': uploaded.name,
            'size': f"{uploaded.size / (1024*1024):.1f} MB",
            'date': datetime.now().strftime("%Y-%m-%d"),
            'type': uploaded.type
        }
        st.session_state.files.insert(0, new_file)
        show_toast(f"Uploaded {uploaded.name}")
        st.rerun()

# ----- Chat Assistant -----
elif current == 'chat':
    # Chat messages
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg['role']):
            st.write(msg['content'])

    # Suggestions
    suggestions = [
        "How do I clone my voice?",
        "What's the difference between instant and premium?",
        "Can I use my cloned voice commercially?",
        "How much storage do I have?"
    ]
    cols = st.columns(len(suggestions))
    for i, sug in enumerate(suggestions):
        if cols[i].button(sug):
            st.session_state.chat_messages.append({'role': 'user', 'content': sug})
            # Simulate response
            time.sleep(1)
            if "clone" in sug.lower():
                resp = "You can start by selecting a clone type from the Voice Cloning page."
            elif "difference" in sug.lower():
                resp = "Instant clone takes 5-10 mins with 30 sec sample, premium takes 2-4 hrs with 10 min sample and higher quality."
            elif "commercial" in sug.lower():
                resp = "Yes, premium clone includes commercial use license."
            elif "storage" in sug.lower():
                resp = "You have 45 MB used out of 1 GB total."
            else:
                resp = "I'm here to help! Please ask about voice cloning, TTS, or storage."
            st.session_state.chat_messages.append({'role': 'assistant', 'content': resp})
            st.rerun()

    # Input
    user_input = st.chat_input("Ask me anything...")
    if user_input:
        st.session_state.chat_messages.append({'role': 'user', 'content': user_input})
        # Simulate response
        with st.spinner("Thinking..."):
            time.sleep(1)
            if "clone" in user_input.lower():
                resp = "You can start by selecting a clone type from the Voice Cloning page."
            elif "difference" in user_input.lower():
                resp = "Instant clone takes 5-10 mins with 30 sec sample, premium takes 2-4 hrs with 10 min sample and higher quality."
            elif "commercial" in user_input.lower():
                resp = "Yes, premium clone includes commercial use license."
            elif "storage" in user_input.lower():
                resp = "You have 45 MB used out of 1 GB total."
            else:
                resp = "I'm here to help! Please ask about voice cloning, TTS, or storage."
            st.session_state.chat_messages.append({'role': 'assistant', 'content': resp})
        st.rerun()

# ----- Settings -----
elif current == 'settings':
    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.subheader("Account Settings")
    email = st.text_input("Email Address", value="mnarayan2703@gmail.com")
    name = st.text_input("Display Name", value="Mohit")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.subheader("Audio Preferences")
    quality = st.selectbox("Default Audio Quality", ["High (320kbps)", "Medium (192kbps)", "Low (128kbps)"], index=1)
    format = st.selectbox("Default Export Format", ["MP3", "WAV", "OGG", "M4A"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.subheader("Notifications")
    email_notif = st.toggle("Email notifications", value=True)
    clone_notif = st.toggle("Clone completion alerts", value=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.subheader("API Configuration")
    api_key = st.text_input("API Key", value="sk_test_abc123xyz789", type="password")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Save Changes", use_container_width=True):
        show_toast("Settings saved (simulated)")

# ----- Profile -----
elif current == 'profile':
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div class="profile-avatar">M</div>
        <h2 style="color: #f1f5f9;">Mohit</h2>
        <p style="color: #94a3b8;">mohit.doe@example.com</p>
        <button class="btn-secondary" style="padding: 0.5rem 1rem;">Edit Profile</button>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.subheader("Subscription Plan")
    st.markdown("""
    <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
        <span>Monthly Clones:</span><span>12 / 50</span>
    </div>
    <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
        <span>Storage:</span><span>45 MB / 1 GB</span>
    </div>
    <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
        <span>Premium Voices:</span><span>3 / 5</span>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Upgrade to Premium", use_container_width=True):
        show_toast("Upgrade feature coming soon!")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.subheader("Usage Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Clones", "12")
        st.metric("Generated Audio", "28")
    with col2:
        st.metric("Total Files", "15")
        st.metric("Member Since", "Oct 2024")
    st.markdown('</div>', unsafe_allow_html=True)