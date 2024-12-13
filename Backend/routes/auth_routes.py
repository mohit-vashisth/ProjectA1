from fastapi import APIRouter, HTTPException, Depends
from ..models.user import User, UserStatus
from ..models.session import Session
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
async def register_user(user_data: dict):
    try:
        # Check if user exists
        existing_user = await User.find_one({"email": user_data["email"]})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        new_user = User(
            username=user_data["username"],
            email=user_data["email"],
            password_hash=user_data["password"],  # Remember to hash password
            status=UserStatus.ACTIVE
        )
        await new_user.save()
        return {"message": "User registered successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
async def login_user(login_data: dict):
    # Add login logic here
    pass 