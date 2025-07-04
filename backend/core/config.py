from dotenv import load_dotenv
import os
from urllib.parse import urlparse

ENVIRONMENT = os.getenv(key="ENV", default="development")

# Load the corresponding .env file
BASE_DIR = os.path.dirname(p=os.path.dirname(p=os.path.dirname(p=os.path.abspath(path=__file__))))
env_new_Path = os.path.join(BASE_DIR, "frontend")
if ENVIRONMENT == "production":
    load_dotenv(dotenv_path=os.path.join(env_new_Path, ".env.production"))
else:
    load_dotenv(dotenv_path=os.path.join(env_new_Path, ".env.development"))

def env_variables(key) -> str:
    value: str | None = os.getenv(key=key)
    if value and value.startswith("http"):
        return urlparse(url=value).path
    return str(object=value)

# API Endpoints
NEW_CHAT_EP = env_variables(key="VITE_NEW_CHAT_EP")
USER_VOICE_ADD_EP = env_variables(key="VITE_USER_VOICE_ADD_EP")
RECENT_FILES_EP = env_variables(key="VITE_RECENT_FILES_EP")
GET_CHATS_FILES_EP = env_variables(key="VITE_GET_CHATS_FILES_EP")
STORAGE_FILES_EP = env_variables(key="VITE_STORAGE_FILES_EP")
LOGOUT_EP = env_variables(key="VITE_LOGOUT_EP")
RENAME_EP = env_variables(key="VITE_RENAME_EP")
TRANSLATE_EP = env_variables(key="VITE_TRANSLATE_SPEECH_EP")
GENERATE_SPEECH_EP = env_variables(key="VITE_GENERATE_SPEECH_EP")
LOGIN_EP = env_variables(key="VITE_LOGIN_EP")
SIGNUP_EP = env_variables(key="VITE_SIGNUP_EP")

# Database Configuration
MONGO_URI = env_variables(key="MONGO_URI")
DATABASE_INIT = env_variables(key="DATABASE_INIT")

# JWT Configuration
PRIVATE_KEY_PATH = env_variables(key="PRIVATE_KEY_PATH")
PUBLIC_KEY_PATH = env_variables(key="PUBLIC_KEY_PATH")
ACCESS_TOKEN_EXPIRE_MINUTES = int(env_variables(key="ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(env_variables(key="REFRESH_TOKEN_EXPIRE_MINUTES"))
JWT_HEADER = {
    "alg":env_variables(key="JWT_ALGORITHM"),
    "typ": env_variables(key="TYPE")
}

# Charator lenth
LENGTH = int(env_variables(key="LENGTH"))

# General App Settings
DEBUG = env_variables(key="DEBUG").strip().lower() in ("true", "1", "yes")
APP_NAME = env_variables(key="APP_NAME")

# APP/API Version
APP_VERSION = env_variables(key="APP_VERSION")

# secret keys init
def read_pv_key():
    with open(PRIVATE_KEY_PATH,'rb') as pv_file:
        pv_key = pv_file.read()

    with open(PUBLIC_KEY_PATH,'rb') as pb_file:
        pb_key = pb_file.read()

    return pv_key, pb_key

MODEL_PATH = env_variables(key="MODEL_PATH_DETECT_LANG")