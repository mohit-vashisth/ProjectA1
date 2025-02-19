from passlib.context import CryptContext
pass_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__time_cost=2,  # Increasing time cost for better security
    argon2__memory_cost=102400,  # Memory cost (16 MB)
    argon2__parallelism=10  # Parallelism (workers)
)

# used to verify the password with stored password in database
def verify_user_password(hashed_password: str, password: str) -> bool:
    return pass_context.verify(password, hashed_password)