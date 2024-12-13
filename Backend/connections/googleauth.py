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

@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for('auth')  # Get the callback URL
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth")
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        user = token.get('userinfo')
        if user:
            # You can store user info in session or return as needed
            return {
                "email": user.email,
                "name": user.name,
                "picture": user.picture
            }
    except Exception as e:
        return {"error": str(e)}
    
    return RedirectResponse(url="/")

@app.get("/logout")
async def logout(request: Request):
    # Clear session or tokens as needed
    return RedirectResponse(url="/")
