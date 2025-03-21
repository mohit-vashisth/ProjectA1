from backend.utils.logger import init_logger

from fastapi import HTTPException, Request, status

def get_cookies_access_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if token:
        init_logger(message=f"token={token}")
        return token

    init_logger(message="token NOT FOUND", level="critical", request=request)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token is not found or valid."
    )

def get_cookies_refresh_token(request: Request) -> str:
    token = request.cookies.get("refresh_token")
    if token:
        init_logger(message=f"token={token}")
        return token

    init_logger(message="token NOT FOUND", level="critical", request=request)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token is not found or valid."
    )
