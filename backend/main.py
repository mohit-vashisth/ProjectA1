from auth.signup import signup_route
from auth.login import login_route
from dashboard.new_chat_service import new_chat_route

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow only frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],
    # max_age=600,  # with this browser will save cache for 10 minutes for development
    # max_age=86400,  # Cache for 1 day in browser this is for production
)

app.include_router(signup_route)
app.include_router(login_route)
app.include_router(new_chat_route)

@app.get("/")
def root() -> dict:
    return {"status": "Success"}