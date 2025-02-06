from auth.signup import signup_route
from auth.login import login_route

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=600,  # with this browser will save cache for 10 minutes for development
    max_age=86400,  # Cache for 1 day in browser this is for production
)


app.include_router(signup_route)
app.include_router(login_route)

@app.get("/")
def root() -> dict:
    return {"status": "Success"}