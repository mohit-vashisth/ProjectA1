from fastapi import APIRouter, HTTPException, Request
from Backend.models.user import User
from beanie import PydanticObjectId
from Backend.connections.googleauth import oauth
from fastapi import Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from typing import Optional

# Initialize the router
router = APIRouter(
    prefix="/users",  # Base path for all user-related routes
    tags=["Users"],  # Tag for API documentation (Swagger UI)
)

# Route to create a new user
@router.post("/", response_model=User)
async def create_user(user: User, request: Request):
    """
    Create a new user and save it to the database.
    """
    # Check if the user already exists
    existing_user = await User.find_one(User.email == user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists.")
    
    # Save the user
    await user.create()
    return user

# Route to get a list of all users
@router.get("/", response_model=list[User])
async def get_users(request: Request):
    """
    Retrieve all users from the database.
    """
    users = await User.find_all().to_list()
    return users

# Route to get a user by ID
@router.get("/{user_id}", response_model=User)
async def get_user(user_id: PydanticObjectId, request: Request):
    """
    Retrieve a user by their ID.
    """
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

# Route to update a user by ID
@router.put("/{user_id}", response_model=User)
async def update_user(user_id: PydanticObjectId, user_data: User, request: Request):
    """
    Update a user's information by their ID.
    """
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    # Update fields
    user.update(user_data.dict(exclude_unset=True))
    await user.save()
    return user

# Route to delete a user by ID
@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: PydanticObjectId, request: Request):
    """
    Delete a user by their ID.
    """
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    await user.delete()
    return {"message": "User deleted successfully."}

@router.get("/google/login")
async def google_login(request: Request):
    """
    Redirect user to Google login page
    """
    redirect_uri = request.url_for('google_auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/auth")
async def google_auth(request: Request):
    """
    Handle Google OAuth callback and create/update user
    """
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')
    
    if user_info:
        # Check if user exists
        existing_user = await User.find_one(User.email == user_info.email)
        
        if existing_user:
            # Update existing user with latest Google info
            existing_user.name = user_info.name
            existing_user.picture = user_info.picture
            await existing_user.save()
            return existing_user
        
        # Create new user from Google info
        new_user = User(
            email=user_info.email,
            name=user_info.name,
            picture=user_info.picture,
            is_google_user=True
        )
        await new_user.create()
        return new_user
    
    raise HTTPException(status_code=400, detail="Failed to get user info from Google")
