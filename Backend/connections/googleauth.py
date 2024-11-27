from authlib.integrations.starlette_client import OAuth 
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.requests import Request
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')


oauth = OAuth()
oauth.register(
    name="google",
    client_id= CLIENT_ID,
    client_secret= CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"}
)
