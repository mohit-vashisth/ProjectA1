from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.auth
from google.auth.transport.requests import Request
from google.oauth2 import id_token

app = FastAPI()

class GoogleToken(BaseModel):
    id_token: str

# Google OAuth2 client ID (jo aapko Google Developer Console se milega)
CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID'

@app.post("/api/auth/google")
async def google_auth(google_token: GoogleToken):
    try:
        # Token ko verify karna
        idinfo = id_token.verify_oauth2_token(google_token.id_token, Request(), CLIENT_ID)

        # Token verify ho gaya
        user_info = {
            "user_id": idinfo['sub'],
            "email": idinfo['email'],
            "name": idinfo['name']
        }

        # User ko authenticate karenge aur database mein save karenge (agar pehli baar hai)
        # For example, save user info into DB or create a JWT token

        return {"success": True, "user_info": user_info}

    except ValueError:
        # Invalid token
        raise HTTPException(status_code=400, detail="Invalid Google Token")
