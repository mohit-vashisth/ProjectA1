from dotenv import load_dotenv
import os
from urllib.parse import urlparse

ENVIRONMENT = os.getenv("ENV", "development")  # Default to development

# Load the corresponding .env file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ENVIRONMENT == "production":
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env.production"))
else:
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env.development"))

def env_variables(key):
    value = os.getenv(key)
    if value and value.startswith("http"):
        return urlparse(value).path
    return value

# API Endpoints
VITE_NEW_CHAT_EP = env_variables("VITE_NEW_CHAT_EP")
VITE_USER_VOICE_ADD_EP = env_variables("VITE_USER_VOICE_ADD_EP")
VITE_RECENT_FILES_EP = env_variables("VITE_RECENT_FILES_EP")
VITE_STORAGE_FILES_EP = env_variables("VITE_STORAGE_FILES_EP")
VITE_LOGOUT_EP = env_variables("VITE_LOGOUT_EP")
VITE_RENAME_EP = env_variables("VITE_RENAME_EP")
VITE_TRANSLATE_SPEECH_EP = env_variables("VITE_TRANSLATE_SPEECH_EP")
VITE_GENERATE_SPEECH_EP = env_variables("VITE_GENERATE_SPEECH_EP")
VITE_LOGIN_EP = env_variables("VITE_LOGIN_EP")
VITE_SIGNUP_EP = env_variables("VITE_SIGNUP_EP")

# Database Configuration
MONGO_URI = env_variables("MONGO_URI")
DATABASE_INIT = env_variables("DATABASE_INIT")

# JWT Configuration
PRIVATE_KEY_PATH = env_variables("PRIVATE_KEY_PATH")
PUBLIC_KEY_PATH = env_variables("PUBLIC_KEY_PATH")
ACCESS_TOKEN_EXPIRE_MINUTES = int(env_variables("ACCESS_TOKEN_EXPIRE_MINUTES"))
JWT_HEADER = {
    "alg":env_variables("JWT_ALGORITHM"),
    "typ": env_variables("TYPE")
}

# CORS Settings
# ALLOWED_ORIGINS = env_variables("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")

# General App Settings
DEBUG = env_variables("DEBUG") == "True"  # Convert string to boolean
APP_NAME = env_variables("APP_NAME")

# secret keys init
def read_pv_key():
    with open(PRIVATE_KEY_PATH,'rb') as pv_file:
        pv_key = pv_file.read()

    with open(PUBLIC_KEY_PATH,'rb') as pb_file:
        pb_key = pb_file.read()

    return pv_key, pb_key