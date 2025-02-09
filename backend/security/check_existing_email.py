from fastapi import HTTPException, status
# Handling existing user email ids
async def check_existing_email(emails: set, requested_email: str, is_signup: bool) -> bool:
    if is_signup and requested_email in emails:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email already in use"
        )
    
    if not is_signup and requested_email not in emails:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No account found with this email"
        )
    return True