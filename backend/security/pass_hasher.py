from passlib.context import CryptContext
pass_context = CryptContext(schemes=["argon2"], deprecated="auto")

# it will take user pass as plain text and then hash
def password_hash(password: str) -> str:
    return pass_context.hash(password)