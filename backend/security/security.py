from passlib.context import CryptContext
pass_context = CryptContext(schemes=["argon2"], deprecated="auto")

# it will take user pass as plain text and then hash
def password_hash(password: str) -> str:
    return pass_context.hash(password)

# used to verify the password with stored password in database
def verify_user_password(password: str, hashed_password: str) -> bool:
    return pass_context.verify(password, hashed_password)