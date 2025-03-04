from passlib.context import CryptContext
from fastapi import HTTPException, status
from backend.utils.logger import init_logger

pass_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__time_cost=2,  # Increasing time cost for better security
    argon2__memory_cost=102400,  # Memory cost (16 MB)
    argon2__parallelism=10  # Parallelism (workers)
)

# used to verify the password with stored password in database
def verify_user_password(hashed_password: str, password: str) -> bool:
    try:
        isPassValid = pass_context.verify(secret=password, hash=hashed_password)
        init_logger(message="Password verified")
        return isPassValid
    except Exception as e:
        init_logger(message=f"Password verification failed: {str(e)}", level="error")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )