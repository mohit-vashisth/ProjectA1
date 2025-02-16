from passlib.context import CryptContext
from fastapi import HTTPException, status
pass_context = CryptContext(schemes=["argon2"], deprecated="auto")

# it will take user pass as plain text and then hash
def password_hash(password: str) -> str:
    return pass_context.hash(password)

# used to verify the password with stored password in database
def verify_user_password(hashed_password: str, password: str) -> bool:
    return pass_context.verify(password, hashed_password)

def check_auth(user_cred: str) -> None:
    user_cred = True #later on we will add logic here that is "JWT Authentication"
    if user_cred:
        return {"status": "Authenticated"}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized"
    )