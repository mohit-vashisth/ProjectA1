from fastapi import FastAPI, Depends
from backend.auth.signup import signup_route
from backend.auth.login import login_route
from backend.dashboard.services.logout_SV import logout_route
from backend.dashboard.services.new_chat_SV import new_chat_route
from backend.dashboard.services.translate_text_SV import translate_route
from backend.security.jwt_handler import verify_n_refresh_token

def include_routers(app: FastAPI):
    app.include_router(router=signup_route, tags=["auth"])
    app.include_router(router=login_route, tags=["auth"])
    app.include_router(router=logout_route, tags=["services"], dependencies=[Depends(verify_n_refresh_token)])
    app.include_router(router=new_chat_route, tags=["services"], dependencies=[Depends(verify_n_refresh_token)])
    app.include_router(router=translate_route, tags=["services"], dependencies=[Depends(verify_n_refresh_token)])
