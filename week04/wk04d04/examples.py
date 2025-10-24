"""
Example extensions for the FastAPI boilerplate.

This file demonstrates how to add common features to your API.
Copy and adapt these examples as needed.
"""

from typing import List, Optional
from datetime import datetime
from enum import Enum

from fastapi import APIRouter, Depends, HTTPException, status, Body
from pydantic import BaseModel, Field, EmailStr, field_validator


# ============================================================================
# EXAMPLE 1: Using APIRouter for modular routing
# ============================================================================

router = APIRouter(
    prefix="/api/v1",
    tags=["examples"],
    responses={404: {"description": "Not found"}}
)


# ============================================================================
# EXAMPLE 2: Advanced Pydantic Models
# ============================================================================

class UserRole(str, Enum):
    """User role enumeration."""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class UserCreate(BaseModel):
    """Model for creating a new user."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.USER
    
    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        """Validate username contains only alphanumeric characters."""
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v


class UserResponse(BaseModel):
    """Model for user response (excludes sensitive data)."""
    id: int
    username: str
    email: EmailStr
    role: UserRole
    created_at: datetime
    is_active: bool = True


class PaginatedResponse(BaseModel):
    """Generic paginated response model."""
    items: List[UserResponse]
    total: int
    page: int
    page_size: int
    has_next: bool


# ============================================================================
# EXAMPLE 3: Dependency Injection
# ============================================================================

async def get_current_user(token: str = Depends(lambda: "fake-token")) -> dict:
    """
    Dependency to get current authenticated user.
    
    In production, this would verify JWT token and fetch user from database.
    """
    if token != "valid-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"id": 1, "username": "testuser", "role": "admin"}


async def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """Dependency to require admin role."""
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


# ============================================================================
# EXAMPLE 4: Advanced Endpoints
# ============================================================================

@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user"
)
async def create_user(
    user: UserCreate = Body(..., example={
        "username": "johndoe",
        "email": "john@example.com",
        "password": "securepass123",
        "role": "user"
    })
) -> UserResponse:
    """
    Create a new user account.
    
    - **username**: Alphanumeric, 3-50 characters
    - **email**: Valid email address
    - **password**: Minimum 8 characters
    - **role**: User role (admin, user, or guest)
    """
    # In production: hash password, save to database
    return UserResponse(
        id=123,
        username=user.username,
        email=user.email,
        role=user.role,
        created_at=datetime.now(),
        is_active=True
    )


@router.get(
    "/users",
    response_model=PaginatedResponse,
    summary="List all users"
)
async def list_users(
    page: int = 1,
    page_size: int = 10,
    role: Optional[UserRole] = None,
    current_user: dict = Depends(get_current_user)
) -> PaginatedResponse:
    """
    Get a paginated list of users.
    
    Requires authentication.
    """
    # Mock data - in production, query from database
    mock_users = [
        UserResponse(
            id=i,
            username=f"user{i}",
            email=f"user{i}@example.com",
            role=UserRole.USER,
            created_at=datetime.now(),
            is_active=True
        )
        for i in range(1, 6)
    ]
    
    return PaginatedResponse(
        items=mock_users,
        total=100,
        page=page,
        page_size=page_size,
        has_next=page * page_size < 100
    )


@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID"
)
async def get_user(
    user_id: int,
    current_user: dict = Depends(get_current_user)
) -> UserResponse:
    """Get a specific user by ID."""
    # Mock data - in production, query from database
    if user_id > 1000:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    
    return UserResponse(
        id=user_id,
        username=f"user{user_id}",
        email=f"user{user_id}@example.com",
        role=UserRole.USER,
        created_at=datetime.now(),
        is_active=True
    )


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user (admin only)"
)
async def delete_user(
    user_id: int,
    admin_user: dict = Depends(require_admin)
) -> None:
    """
    Delete a user account.
    
    Requires admin role.
    """
    # In production: delete from database
    pass


# ============================================================================
# EXAMPLE 5: File Upload
# ============================================================================

from fastapi import File, UploadFile


@router.post(
    "/upload",
    summary="Upload a file"
)
async def upload_file(
    file: UploadFile = File(..., description="File to upload"),
    current_user: dict = Depends(get_current_user)
) -> dict:
    """
    Upload a file.
    
    Maximum file size should be configured in production.
    """
    contents = await file.read()
    
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents),
        "uploaded_by": current_user["username"]
    }


# ============================================================================
# EXAMPLE 6: Background Tasks
# ============================================================================

from fastapi import BackgroundTasks
import asyncio


async def send_notification(email: str, message: str):
    """Simulate sending a notification."""
    await asyncio.sleep(2)  # Simulate delay
    print(f"Notification sent to {email}: {message}")


@router.post(
    "/notify",
    summary="Send notification"
)
async def create_notification(
    email: EmailStr,
    message: str,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
) -> dict:
    """
    Create a notification that will be sent in the background.
    """
    background_tasks.add_task(send_notification, email, message)
    
    return {
        "message": "Notification queued",
        "email": email
    }


# ============================================================================
# EXAMPLE 7: WebSocket Support
# ============================================================================

from fastapi import WebSocket, WebSocketDisconnect


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    """
    WebSocket endpoint for real-time communication.
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message from client {client_id}: {data}")
    except WebSocketDisconnect:
        print(f"Client {client_id} disconnected")


# ============================================================================
# To use these examples, add to your main app:
# 
# from examples import router as examples_router
# app.include_router(examples_router)
# ============================================================================
