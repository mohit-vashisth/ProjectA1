from fastapi import APIRouter, Cookie, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from backend.core import config
from backend.security.jwt_handler import verify_n_refresh_token
from backend.security.token_verification import validate_refresh_token
from backend.utils.logger import init_logger


refresh_token_route = APIRouter()

@refresh_token_route.post(path=config.VITE_REFRESH_TOKEN_EP)
async def refresh_token_sv(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    access_token = request.cookies.get("access_token")
    if access_token:
        await verify_n_refresh_token(request=request)
        init_logger(message="Access token still exist cannot create new one.", level="error")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="access token already exist"
        )
    await validate_refresh_token(refresh_token=refresh_token)
    new_access_token = await verify_n_refresh_token(request=request)
    response.set_cookie(
            key = "access_token",
            value = new_access_token,
            httponly=True,
            secure=not config.DEBUG,
            samesite="lax",
            max_age=600 if config.DEBUG else 86400
        )
    return JSONResponse(
            content= {
                "message": "New access token created successfully."
            },
            headers={"X-API-Version": config.APP_VERSION, **response.headers}
        )

    