from passlib.context import CryptContext
pass_context = CryptContext(schemes=["argon2"], deprecated="auto")

# used to verify the password with stored password in database
def verify_user_password(hashed_password: str, password: str) -> bool:
    return pass_context.verify(password, hashed_password)