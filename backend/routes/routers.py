from fastapi import FastAPI, Depends
from backend.auth.signup import signup_route
from backend.auth.login import login_route
from backend.dashboard.services.logout_SV import logout_route
from backend.dashboard.services.new_chat_SV import new_chat_route
from backend.dashboard.services.translate_text_SV import translate_route
from backend.security.token_verification import verify_n_refresh_token
from backend.core.config import DEBUG

def include_routers(app: FastAPI):
    auth_routes: list[tuple] = [
        (translate_route, ["services"]),
        (logout_route, ["auth"]),
        (new_chat_route, ["services"])
    ]

    app.include_router(router=signup_route, tags=["auth"])
    app.include_router(router=login_route, tags=["auth"])

    for route, tags in auth_routes:
        if not DEBUG:
            app.include_router(router=route, tags=tags)
        else:
            app.include_router(router=route, tags=tags, dependencies=[Depends(dependency=verify_n_refresh_token)])

