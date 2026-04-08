from pathlib import Path
from dotenv import load_dotenv
import os
from urllib.parse import urlparse

# =========================
# 🧭 Base directory (Project root)
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# =========================
# 🔄 Load environment variables (SAFE + FORCE)
# =========================
ENV_PATH = (BASE_DIR / ".env.development").resolve()

if not ENV_PATH.exists():
    raise FileNotFoundError(f"❌ .env file not found at: {ENV_PATH}")

load_dotenv(dotenv_path=str(ENV_PATH), override=True)

# =========================
# 🌍 Detect environment
# =========================
ENVIRONMENT = os.getenv("ENV", "development")

# =========================
# 🧠 Helper function
# =========================
def env_variables(key: str) -> str:
    value = os.getenv(key)

    if value is None:
        raise ValueError(f"❌ Missing environment variable: {key}")

    if isinstance(value, str) and value.startswith("http"):
        return urlparse(value).path

    return value


# =========================
# 🔗 API Endpoints
# =========================
NEW_CHAT_EP = env_variables("VITE_NEW_CHAT_EP")
USER_VOICE_ADD_EP = env_variables("VITE_USER_VOICE_ADD_EP")
RECENT_FILES_EP = env_variables("VITE_RECENT_CHATS_FILES_EP")
GET_CHATS_FILES_EP = env_variables("VITE_GET_CHATS_FILES_EP")
STORAGE_FILES_EP = env_variables("VITE_STORAGE_FILES_EP")
LOGOUT_EP = env_variables("VITE_LOGOUT_EP")
RENAME_EP = env_variables("VITE_RENAME_EP")
TRANSLATE_EP = env_variables("VITE_TRANSLATE_SPEECH_EP")
GENERATE_SPEECH_EP = env_variables("VITE_GENERATE_SPEECH_EP")
LOGIN_EP = env_variables("VITE_LOGIN_EP")
SIGNUP_EP = env_variables("VITE_SIGNUP_EP")


# =========================
# 🗄️ Database
# =========================
MONGO_URI = env_variables("MONGO_URI")
DATABASE_INIT = env_variables("DATABASE_INIT")


# =========================
# 🔐 JWT
# =========================
PRIVATE_KEY_PATH = BASE_DIR / env_variables("PRIVATE_KEY_PATH")
PUBLIC_KEY_PATH = BASE_DIR / env_variables("PUBLIC_KEY_PATH")

ACCESS_TOKEN_EXPIRE_MINUTES = int(env_variables("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(env_variables("REFRESH_TOKEN_EXPIRE_MINUTES"))

JWT_HEADER = {
    "alg": env_variables("JWT_ALGORITHM"),
    "typ": env_variables("TYPE"),
}


# =========================
# 📏 Misc
# =========================
LENGTH = int(env_variables("LENGTH"))

DEBUG = env_variables("DEBUG").strip().lower() in ("true", "1", "yes")

APP_NAME = env_variables("APP_NAME")
APP_VERSION = env_variables("APP_VERSION")


# =========================
# 🔑 Read Keys
# =========================
def read_pv_key():
    pv_key = PRIVATE_KEY_PATH.read_bytes()
    pb_key = PUBLIC_KEY_PATH.read_bytes()
    return pv_key, pb_key


# =========================
# 🤖 Model
# =========================
MODEL_PATH = str(BASE_DIR / env_variables("MODEL_PATH_DETECT_LANG"))


# =========================
# 🧪 DEBUG (remove later)
# =========================