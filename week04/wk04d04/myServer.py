"""
FastAPI Boilerplate Application

A well-structured FastAPI application following best practices including:
- Pydantic models for request/response validation
- Proper type hints
- API versioning
- CORS configuration
- Structured error handling
- Clean separation of concerns
- Professional logging with custom logger module
"""

from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query, Path, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ConfigDict
import uvicorn

# Import our custom logger
from myLogger import get_logger, log_execution_time


# Configure logging using our custom logger module
logger = get_logger(__name__)


# Pydantic Models
class HealthCheck(BaseModel):
    """Response model for health check endpoint."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")


class Item(BaseModel):
    """Item model with validation."""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "item_id": 42,
            "q": "search query",
            "description": "Optional description"
        }
    })
    
    item_id: int = Field(..., gt=0, description="Unique item identifier")
    q: Optional[str] = Field(None, description="Optional query parameter")
    description: Optional[str] = Field(None, description="Item description")


class UserItem(BaseModel):
    """User item model with owner information."""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "item_id": 42,
            "owner_id": 1,
            "q": "search query",
            "description": "This is a short description"
        }
    })
    
    item_id: int = Field(..., gt=0, description="Unique item identifier")
    owner_id: int = Field(..., gt=0, description="User ID of the owner")
    q: Optional[str] = Field(None, description="Optional query parameter")
    description: Optional[str] = Field(None, description="Item description")


class Message(BaseModel):
    """Generic message response model."""
    message: str = Field(..., description="Response message")


# Application lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown events."""
    # Startup
    logger.info("Starting up FastAPI application...")
    yield
    # Shutdown
    logger.info("Shutting down FastAPI application...")


# Initialize FastAPI app
app = FastAPI(
    title="FastAPI Boilerplate",
    description="A production-ready FastAPI boilerplate with best practices",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Handle HTTP exceptions with consistent error responses."""
    logger.error(f"HTTP error occurred: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """Handle unexpected exceptions gracefully."""
    logger.error(f"Unexpected error occurred: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error", "status_code": 500}
    )


# API Routes
@app.get(
    "/",
    response_model=Message,
    tags=["Root"],
    summary="Root endpoint",
    description="Welcome message for the API"
)
async def read_root() -> Message:
    """
    Root endpoint returning a welcome message.
    
    Returns:
        Message: Welcome message object
    """
    logger.info("Root endpoint accessed")
    return Message(message="Welcome to FastAPI Boilerplate!")


@app.get(
    "/health",
    response_model=HealthCheck,
    tags=["Health"],
    summary="Health check",
    description="Check the health status of the API"
)
async def health_check() -> HealthCheck:
    """
    Health check endpoint for monitoring.
    
    Returns:
        HealthCheck: Service health status and version
    """
    return HealthCheck(status="healthy", version="1.0.0")


@app.get(
    "/api/v1/items/{item_id}",
    response_model=Item,
    tags=["Items"],
    summary="Get item by ID",
    description="Retrieve a specific item by its unique identifier",
    responses={
        200: {"description": "Item found successfully"},
        404: {"description": "Item not found"}
    }
)
async def read_item(
    item_id: int = Path(..., gt=0, description="The ID of the item to retrieve"),
    q: Optional[str] = Query(None, min_length=1, max_length=50, description="Optional search query")
) -> Item:
    """
    Get an item by ID with optional query parameter.
    
    Args:
        item_id: Unique identifier for the item (must be positive)
        q: Optional query string for filtering
        
    Returns:
        Item: The requested item details
        
    Raises:
        HTTPException: If item_id is invalid
    """
    logger.info(f"Fetching item with ID: {item_id}")
    
    # Example validation
    if item_id > 1000:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    
    return Item(item_id=item_id, q=q)


@app.get(
    "/api/v1/users/{user_id}/items/{item_id}",
    response_model=UserItem,
    tags=["Users", "Items"],
    summary="Get user's item",
    description="Retrieve a specific item belonging to a user",
    responses={
        200: {"description": "User item found successfully"},
        404: {"description": "User or item not found"}
    }
)
async def read_user_item(
    user_id: int = Path(..., gt=0, description="The ID of the user"),
    item_id: int = Path(..., gt=0, description="The ID of the item"),
    q: Optional[str] = Query(None, min_length=1, max_length=50, description="Optional search query"),
    short: bool = Query(False, description="Return short description")
) -> UserItem:
    """
    Get a specific item owned by a user.
    
    Args:
        user_id: User's unique identifier (must be positive)
        item_id: Item's unique identifier (must be positive)
        q: Optional query string for filtering
        short: If True, includes a short description
        
    Returns:
        UserItem: The requested user item with details
        
    Raises:
        HTTPException: If user_id or item_id is invalid
    """
    logger.info(f"Fetching item {item_id} for user {user_id}")
    
    # Example validation
    if user_id > 1000 or item_id > 1000:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User or item not found"
        )
    
    description = "This is a short description" if short else None
    
    return UserItem(
        item_id=item_id,
        owner_id=user_id,
        q=q,
        description=description
    )


# Application entry point
if __name__ == "__main__":
    """Run the application with uvicorn."""
    uvicorn.run(
        "myServer:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload during development
        log_level="info"
    )