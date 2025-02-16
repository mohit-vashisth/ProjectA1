from fastapi import HTTPException, status
from database.find_user import get_user
async def check_existing_email(req_email: str, is_signup: bool = True) -> bool:
    user_data = await get_user(req_email)
    # Debugging ke liye add ki line 
    print(f"Checking email: {req_email}, Found user: {user_data}")

    if is_signup and user_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already in use"
        )
    
    if not is_signup and not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No account found with this email"
        )
    
    return True
