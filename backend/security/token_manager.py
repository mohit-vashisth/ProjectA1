from fastapi import HTTPException, Request, status
from backend.utils.logger import init_logger

def get_cookies_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if token:
        init_logger(message=f"token={token}")
        return token

    init_logger(message="token NOT FOUND")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token is not found or valid."
    )
