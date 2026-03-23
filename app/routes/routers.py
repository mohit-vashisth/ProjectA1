from app.core.config import DEBUG
from app.auth.login import login_route
from app.auth.signup import signup_route
from app.dashboard.services.logout_SV import logout_route
from app.dashboard.services.new_chat_SV import new_chat_route
from app.dashboard.services.add_voice_SV import user_voice_route
from app.dashboard.services.delete_chat_SV import delete_chat_route
from app.dashboard.services.rename_chat_SV import rename_chat_route
from app.security.token_verification import verify_and_refresh_token
from app.dashboard.services.translate_text_SV import translate_route
from app.dashboard.services.storage_file_SV import storage_file_route

from fastapi import FastAPI, Depends

def include_routers(app: FastAPI):
    auth_routes: list[tuple] = [
        (logout_route, ["auth"]),
        (translate_route, ["services"]),
        (user_voice_route, ["services"]),
        (rename_chat_route, ["services"]),
        (delete_chat_route, ["services"]),
        (storage_file_route, ["services"]),
    ]

    for route, tags in auth_routes:
        if DEBUG:
            app.include_router(router=route, tags=tags)
        app.include_router(router=route, tags=tags, dependencies=[Depends(dependency=verify_and_refresh_token)])

    app.include_router(router=login_route, tags=["auth"])
    app.include_router(router=signup_route, tags=["auth"])


