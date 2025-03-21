from backend.utils.logger import init_logger

from authlib.jose import JWTClaims
from fastapi import HTTPException, status


def get_jwt_email(decoded_token: str) -> str:
    try:
        if isinstance(decoded_token, JWTClaims):
            init_logger(message="Extracting Email Id from JWTClaims")
            email_id = decoded_token.get("email_ID")
            if email_id is None:
                init_logger(message="Email Id not found in JWTClaims.", level="error")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email Id not found in JWTClaims"
                )
            return str(email_id)
        else:
            init_logger(message="Invalid payload type: Expected JWTClaims instance", level="error")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid payload type: Expected JWTClaims instance"
            )
    except HTTPException as e:
        init_logger(message=f"error while extracting email: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="error while extracting email_id"
        )