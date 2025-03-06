from fastapi import APIRouter, HTTPException, Request, status
from backend.core import config
from backend.utils.logger import init_logger

logout_route = APIRouter()
@logout_route.post(path=config.VITE_LOGOUT_EP, status_code=status.HTTP_200_OK)
def logout(request: Request):
    init_logger(message=f"method :{request.method} | url:{request.url} | cookies: {request.cookies}")
    