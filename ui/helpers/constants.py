# constants.py

# -----------------------------
# APP CONFIG
# -----------------------------

APP_NAME = "Mirage"
APP_VERSION = "1.0.0"

# -----------------------------
# ROUTES
# -----------------------------

ROUTE_HOME = "home"
ROUTE_GENERATE = "generate"
ROUTE_VOICES = "voices"

ALL_ROUTES = [
    ROUTE_HOME,
    ROUTE_GENERATE,
    ROUTE_VOICES,
]

DEFAULT_ROUTE = ROUTE_HOME

# -----------------------------
# BOTTOM NAV CONFIG
# -----------------------------

BOTTOM_NAV_ITEMS = [
    {
        "id": ROUTE_HOME,
        "label": "Home",
        "icon": "🏠",
    },
    {
        "id": ROUTE_GENERATE,
        "label": "Generate",
        "icon": "🎙️",
    },
    {
        "id": ROUTE_VOICES,
        "label": "Voices",
        "icon": "🧠",
    },
]

# -----------------------------
# FILE UPLOAD
# -----------------------------

SUPPORTED_AUDIO_FORMATS = ["wav", "mp3", "ogg"]
MAX_FILE_SIZE_MB = 25


# -----------------------------
# TEXT / GENERATION DEFAULTS
# -----------------------------

DEFAULT_LANGUAGE = "en"
DEFAULT_VOICE_STYLE = "neutral"
MAX_TEXT_LENGTH = 5000

# -----------------------------
# BUTTON LABELS
# -----------------------------

BTN_GENERATE = "Generate Voice"
BTN_UPLOAD = "Upload Audio"
BTN_PLAY = "Play"
BTN_STOP = "Stop"
BTN_DOWNLOAD = "Download"
BTN_REGENERATE = "Regenerate"

# -----------------------------
# UI STATES
# -----------------------------

STATE_ROUTE = "route"
STATE_UPLOADED_FILE = "uploaded_file"
STATE_GENERATED_AUDIO = "generated_audio"
STATE_SELECTED_VOICE = "selected_voice"

# -----------------------------
# API CONFIG (future use)
# -----------------------------

API_BASE_URL = "http://localhost:8000"

# Endpoints (keep aligned with FastAPI)
API_GENERATE = "/generate"
API_UPLOAD = "/upload"
API_VOICES = "/voices"

# -----------------------------
# ERROR MESSAGES
# -----------------------------

ERROR_NO_FILE = "Please upload an audio file."
ERROR_NO_TEXT = "Please enter text."
ERROR_GENERATION_FAILED = "Voice generation failed. Try again."

# -----------------------------
# SUCCESS MESSAGES
# -----------------------------

SUCCESS_UPLOAD = "File uploaded successfully."
SUCCESS_GENERATED = "Voice generated successfully."