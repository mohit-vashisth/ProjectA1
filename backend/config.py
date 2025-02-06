from dotenv import load_dotenv
import os
from urllib.parse import urlparse

ENVIRONMENT = os.getenv("ENV", "development")  # Default to development

# Load the corresponding .env file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ENVIRONMENT == "production":
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env.production"))
else:
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env.development"))

def env_variables(key):
    value = os.getenv(key)
    if value and value.startswith("http"):
        return urlparse(value).path