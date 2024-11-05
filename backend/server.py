
import firebase_admin
from firebase_admin import credentials, auth

# Load the service account key JSON file
cred = credentials.Certificate("backend/serviceAccountKey.json")

# Initialize the Firebase Admin SDK
firebase_admin.initialize_app(cred)

# verify_firebase_token

def verify_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token['uid']
    except Exception as e:
        print("Token verification failed:", e)
        return None
