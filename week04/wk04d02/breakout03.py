"""
W4D2 Breakout Activity 1: Personal Information API
===================================================

This module implements a complete RESTful API for managing personal information
and hobbies using FastAPI with proper validation, error handling, and HTTP methods.

Features:
- CRUD operations for personal information
- CRUD operations for hobbies
- Request/response validation using Pydantic
- Proper HTTP status codes
- Query parameter filtering
- Statistics endpoint

Learning Objectives:
- Understanding REST principles
- Using FastAPI for API development
- Implementing Pydantic models for validation
- Proper error handling with HTTP exceptions
- Testing APIs with interactive documentation

Author: EHunt
Date: October 21, 2025
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime

# ============================================
# FASTAPI APPLICATION SETUP
# ============================================

app = FastAPI(
    title="Personal Information API",
    description="Manage personal information and hobbies via REST API",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI documentation
    redoc_url="/redoc"  # ReDoc documentation
)

# ============================================
# PYDANTIC MODELS (Data Validation)
# ============================================

class PersonalInfo(BaseModel):
    """
    Personal information model with validation.
    
    This model ensures that all personal data meets the required constraints
    before being stored or returned to the client.
    """
    name: str = Field(..., min_length=1, max_length=100, description="Full name")
    age: int = Field(..., ge=0, le=150, description="Age in years")
    location: str = Field(..., min_length=1, description="Current location")
    occupation: str = Field(..., min_length=1, description="Current occupation")
    bio: Optional[str] = Field(None, max_length=500, description="Short biography")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "age": 28,
                "location": "San Francisco, CA",
                "occupation": "ML Engineer",
                "bio": "Passionate about AI and building scalable systems"
            }
        }
    )
    
    @field_validator('age')
    @classmethod
    def age_must_be_realistic(cls, v):
        """Validate that age is within realistic bounds."""
        if v < 0 or v > 150:
            raise ValueError('Age must be between 0 and 150')
        return v


class Hobby(BaseModel):
    """
    Hobby model with validation for creating new hobbies.
    
    This model enforces skill level constraints and ensures
    all required fields are provided.
    """
    name: str = Field(..., min_length=1, max_length=100, description="Hobby name")
    skill_level: str = Field(
        ..., 
        pattern="^(beginner|intermediate|advanced|expert)$",
        description="Skill level (beginner, intermediate, advanced, expert)"
    )
    years_experience: int = Field(..., ge=0, le=100, description="Years of experience")
    description: Optional[str] = Field(None, max_length=500, description="Hobby description")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Photography",
                "skill_level": "intermediate",
                "years_experience": 3,
                "description": "Love capturing landscapes and portraits"
            }
        }
    )
    
    @field_validator('skill_level')
    @classmethod
    def validate_skill_level(cls, v):
        """Ensure skill level is lowercase for consistency."""
        return v.lower()


class HobbyUpdate(BaseModel):
    """
    Model for updating hobby (all fields optional).
    
    This allows partial updates where only specified fields are modified.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    skill_level: Optional[str] = Field(
        None, 
        pattern="^(beginner|intermediate|advanced|expert)$"
    )
    years_experience: Optional[int] = Field(None, ge=0, le=100)
    description: Optional[str] = Field(None, max_length=500)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "skill_level": "advanced",
                "years_experience": 5
            }
        }
    )
    
    @field_validator('skill_level')
    @classmethod
    def validate_skill_level(cls, v):
        """Ensure skill level is lowercase for consistency."""
        if v is not None:
            return v.lower()
        return v


class HobbyResponse(BaseModel):
    """
    Response model for hobby with ID included.
    
    This is returned when retrieving hobbies from the database.
    """
    id: int = Field(..., description="Unique hobby identifier")
    name: str
    skill_level: str
    years_experience: int
    description: Optional[str]
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Programming",
                "skill_level": "intermediate",
                "years_experience": 2,
                "description": "Love building Python applications"
            }
        }
    )


# ============================================
# IN-MEMORY DATA STORAGE
# ============================================

# Personal information database (singleton-like data)
# In production, this would be stored in a database
personal_info_db: Dict[str, Any] = {
    "name": "Alex Johnson",
    "age": 26,
    "location": "Seattle, WA",
    "occupation": "ML Engineer in Training",
    "bio": "Learning to build amazing APIs and ML systems!"
}

# Hobbies database (simulating a table in a database)
# In production, this would be stored in a database with proper indexing
hobbies_db: List[Dict[str, Any]] = [
    {
        "id": 1,
        "name": "Programming",
        "skill_level": "intermediate",
        "years_experience": 2,
        "description": "Love building Python applications and APIs"
    },
    {
        "id": 2,
        "name": "Machine Learning",
        "skill_level": "beginner",
        "years_experience": 1,
        "description": "Exploring AI and data science fundamentals"
    },
    {
        "id": 3,
        "name": "Rock Climbing",
        "skill_level": "advanced",
        "years_experience": 5,
        "description": "Outdoor bouldering and sport climbing enthusiast"
    }
]

# Global counter for generating unique hobby IDs
# In production, this would be handled by database auto-increment
hobby_id_counter: int = 4


# ============================================
# HELPER FUNCTIONS
# ============================================

def find_hobby_by_id(hobby_id: int) -> Optional[Dict[str, Any]]:
    """
    Find a hobby in the database by its ID.
    
    Args:
        hobby_id: The unique identifier of the hobby
        
    Returns:
        The hobby dictionary if found, None otherwise
    """
    for hobby in hobbies_db:
        if hobby["id"] == hobby_id:
            return hobby
    return None


def remove_hobby_by_id(hobby_id: int) -> bool:
    """
    Remove a hobby from the database by its ID.
    
    Args:
        hobby_id: The unique identifier of the hobby
        
    Returns:
        True if hobby was removed, False if not found
    """
    hobby = find_hobby_by_id(hobby_id)
    if hobby:
        hobbies_db.remove(hobby)
        return True
    return False


# ============================================
# API ENDPOINTS - PERSONAL INFORMATION
# ============================================

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint providing API information.
    
    This helps users discover the API capabilities.
    """
    return {
        "message": "Welcome to the Personal Information API",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "personal_info": "/me",
            "hobbies": "/hobbies",
            "statistics": "/stats"
        }
    }


@app.get("/me", response_model=PersonalInfo, tags=["Personal Info"])
async def get_personal_info():
    """
    Retrieve your personal information.
    
    Returns:
        PersonalInfo: Current personal information from the database
        
    Example Response:
        {
            "name": "Alex Johnson",
            "age": 26,
            "location": "Seattle, WA",
            "occupation": "ML Engineer in Training",
            "bio": "Learning to build amazing APIs!"
        }
    """
    # Return the personal info database as a validated Pydantic model
    # This ensures the response matches the expected schema
    return PersonalInfo(**personal_info_db)


@app.put("/me", response_model=PersonalInfo, tags=["Personal Info"])
async def update_personal_info(info: PersonalInfo):
    """
    Update your personal information.
    
    This endpoint allows you to update all personal information fields.
    All fields are required for a PUT request (full update).
    
    Args:
        info: Updated personal information (validated by Pydantic)
        
    Returns:
        PersonalInfo: The updated personal information
        
    Example Request:
        {
            "name": "Alex Johnson",
            "age": 27,
            "location": "Portland, OR",
            "occupation": "Senior ML Engineer",
            "bio": "Building production ML systems"
        }
    """
    # Convert Pydantic model to dictionary and update database
    # Using .dict() ensures we get a clean dictionary representation
    personal_info_db.update(info.dict())
    
    # Return the updated information
    return PersonalInfo(**personal_info_db)


# ============================================
# API ENDPOINTS - HOBBIES CRUD
# ============================================

@app.get("/hobbies", response_model=List[HobbyResponse], tags=["Hobbies"])
async def get_hobbies(
    skill_level: Optional[str] = None,
    min_experience: Optional[int] = None
):
    """
    Get list of all hobbies with optional filtering.
    
    This endpoint supports query parameters for filtering results.
    If no filters are provided, all hobbies are returned.
    
    Args:
        skill_level: Filter by skill level (beginner/intermediate/advanced/expert)
        min_experience: Filter by minimum years of experience
        
    Returns:
        List[HobbyResponse]: List of hobbies matching the filter criteria
        
    Examples:
        - GET /hobbies - Returns all hobbies
        - GET /hobbies?skill_level=intermediate - Returns intermediate level hobbies
        - GET /hobbies?min_experience=3 - Returns hobbies with 3+ years experience
        - GET /hobbies?skill_level=advanced&min_experience=4 - Combined filters
    """
    # Start with all hobbies
    filtered_hobbies = hobbies_db.copy()
    
    # Apply skill level filter if provided
    if skill_level:
        # Normalize to lowercase for case-insensitive comparison
        skill_level_lower = skill_level.lower()
        
        # Validate skill level
        valid_levels = ["beginner", "intermediate", "advanced", "expert"]
        if skill_level_lower not in valid_levels:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid skill level. Must be one of: {', '.join(valid_levels)}"
            )
        
        # Filter by skill level
        filtered_hobbies = [
            h for h in filtered_hobbies 
            if h["skill_level"] == skill_level_lower
        ]
    
    # Apply minimum experience filter if provided
    if min_experience is not None:
        # Validate minimum experience
        if min_experience < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Minimum experience must be non-negative"
            )
        
        # Filter by minimum experience
        filtered_hobbies = [
            h for h in filtered_hobbies 
            if h["years_experience"] >= min_experience
        ]
    
    # Convert to response models for proper validation
    return [HobbyResponse(**hobby) for hobby in filtered_hobbies]


@app.get("/hobbies/{hobby_id}", response_model=HobbyResponse, tags=["Hobbies"])
async def get_hobby(hobby_id: int):
    """
    Get details of a specific hobby by ID.
    
    Args:
        hobby_id: The unique identifier of the hobby
        
    Returns:
        HobbyResponse: The requested hobby details
        
    Raises:
        HTTPException 404: If hobby with given ID is not found
        
    Example:
        GET /hobbies/1 - Returns hobby with ID 1
    """
    # Find the hobby in the database
    hobby = find_hobby_by_id(hobby_id)
    
    # Return 404 if hobby doesn't exist
    if not hobby:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hobby with ID {hobby_id} not found"
        )
    
    # Return the hobby as a validated response model
    return HobbyResponse(**hobby)


@app.post("/hobbies", response_model=HobbyResponse, status_code=status.HTTP_201_CREATED, tags=["Hobbies"])
async def add_hobby(hobby: Hobby):
    """
    Add a new hobby to your collection.
    
    This endpoint creates a new hobby with an auto-generated ID.
    Returns 201 Created status code on success.
    
    Args:
        hobby: New hobby information (validated by Pydantic)
        
    Returns:
        HobbyResponse: The created hobby with its assigned ID
        
    Example Request:
        {
            "name": "Guitar",
            "skill_level": "beginner",
            "years_experience": 1,
            "description": "Learning acoustic guitar"
        }
        
    Example Response (201 Created):
        {
            "id": 4,
            "name": "Guitar",
            "skill_level": "beginner",
            "years_experience": 1,
            "description": "Learning acoustic guitar"
        }
    """
    global hobby_id_counter
    
    # Create new hobby dictionary with auto-generated ID
    new_hobby = {
        "id": hobby_id_counter,
        **hobby.dict()  # Unpack all hobby fields from Pydantic model
    }
    
    # Add to database
    hobbies_db.append(new_hobby)
    
    # Increment counter for next hobby
    hobby_id_counter += 1
    
    # Return the created hobby with 201 status
    return HobbyResponse(**new_hobby)


@app.put("/hobbies/{hobby_id}", response_model=HobbyResponse, tags=["Hobbies"])
async def update_hobby(hobby_id: int, hobby_update: HobbyUpdate):
    """
    Update an existing hobby.
    
    This endpoint allows partial updates - only provided fields will be updated.
    Fields not included in the request will remain unchanged.
    
    Args:
        hobby_id: ID of the hobby to update
        hobby_update: Fields to update (all optional for partial updates)
        
    Returns:
        HobbyResponse: The updated hobby
        
    Raises:
        HTTPException 404: If hobby with given ID is not found
        
    Example Request (partial update):
        {
            "skill_level": "advanced",
            "years_experience": 6
        }
    """
    # Find the hobby to update
    hobby = find_hobby_by_id(hobby_id)
    
    # Return 404 if hobby doesn't exist
    if not hobby:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hobby with ID {hobby_id} not found"
        )
    
    # Update only the fields that were provided
    # exclude_unset=True means only explicitly set fields are included
    update_data = hobby_update.dict(exclude_unset=True)
    
    # Apply updates to the hobby
    for field, value in update_data.items():
        hobby[field] = value
    
    # Return the updated hobby
    return HobbyResponse(**hobby)


@app.delete("/hobbies/{hobby_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Hobbies"])
async def delete_hobby(hobby_id: int):
    """
    Delete a hobby from your collection.
    
    This endpoint removes a hobby permanently from the database.
    Returns 204 No Content on successful deletion.
    
    Args:
        hobby_id: ID of the hobby to delete
        
    Raises:
        HTTPException 404: If hobby with given ID is not found
        
    Response:
        204 No Content (empty response body on success)
    """
    # Attempt to remove the hobby
    removed = remove_hobby_by_id(hobby_id)
    
    # Return 404 if hobby doesn't exist
    if not removed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hobby with ID {hobby_id} not found"
        )
    
    # 204 No Content - successful deletion with no response body
    # FastAPI automatically handles this when we don't return anything
    return


# ============================================
# BONUS ENDPOINTS
# ============================================

@app.get("/stats", tags=["Statistics"])
async def get_stats():
    """
    Get comprehensive statistics about your hobbies.
    
    This endpoint calculates various metrics from your hobby collection,
    including totals, averages, and distributions.
    
    Returns:
        Dictionary containing statistics:
        - total_hobbies: Total number of hobbies
        - average_experience: Average years of experience across all hobbies
        - total_experience: Total years of experience combined
        - skill_level_distribution: Count of hobbies at each skill level
        - most_experienced_hobby: Hobby with the most years of experience
        - least_experienced_hobby: Hobby with the least years of experience
        
    Example Response:
        {
            "total_hobbies": 3,
            "average_experience": 2.67,
            "total_experience": 8,
            "skill_level_distribution": {
                "beginner": 1,
                "intermediate": 1,
                "advanced": 1,
                "expert": 0
            },
            "most_experienced_hobby": {
                "name": "Rock Climbing",
                "years_experience": 5
            },
            "least_experienced_hobby": {
                "name": "Machine Learning",
                "years_experience": 1
            }
        }
    """
    # Handle empty database case
    if not hobbies_db:
        return {
            "total_hobbies": 0,
            "average_experience": 0,
            "total_experience": 0,
            "skill_level_distribution": {
                "beginner": 0,
                "intermediate": 0,
                "advanced": 0,
                "expert": 0
            },
            "most_experienced_hobby": None,
            "least_experienced_hobby": None
        }
    
    # Calculate total hobbies
    total_hobbies = len(hobbies_db)
    
    # Calculate total and average experience
    total_experience = sum(h["years_experience"] for h in hobbies_db)
    average_experience = round(total_experience / total_hobbies, 2)
    
    # Calculate skill level distribution
    skill_distribution = {
        "beginner": 0,
        "intermediate": 0,
        "advanced": 0,
        "expert": 0
    }
    
    for hobby in hobbies_db:
        skill_level = hobby["skill_level"]
        if skill_level in skill_distribution:
            skill_distribution[skill_level] += 1
    
    # Find most and least experienced hobbies
    most_experienced = max(hobbies_db, key=lambda h: h["years_experience"])
    least_experienced = min(hobbies_db, key=lambda h: h["years_experience"])
    
    # Compile statistics
    stats = {
        "total_hobbies": total_hobbies,
        "average_experience": average_experience,
        "total_experience": total_experience,
        "skill_level_distribution": skill_distribution,
        "most_experienced_hobby": {
            "name": most_experienced["name"],
            "years_experience": most_experienced["years_experience"]
        },
        "least_experienced_hobby": {
            "name": least_experienced["name"],
            "years_experience": least_experienced["years_experience"]
        }
    }
    
    return stats


@app.get("/health", tags=["System"])
async def health_check():
    """
    Health check endpoint for monitoring.
    
    This endpoint is useful for container orchestration systems,
    load balancers, and monitoring tools to verify the API is running.
    
    Returns:
        Dictionary with status and timestamp
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Personal Information API",
        "version": "1.0.0"
    }


# ============================================
# RUN THE SERVER
# ============================================

if __name__ == "__main__":
    import uvicorn
    
    print("="*60)
    print("🚀 Starting Personal Information API...")
    print("="*60)
    print()
    print("📖 Swagger Documentation: http://localhost:8000/docs")
    print("📚 ReDoc Documentation:   http://localhost:8000/redoc")
    print()
    print("🧪 Available Endpoints:")
    print("   GET    /               - API information")
    print("   GET    /health         - Health check")
    print("   GET    /me             - Get personal info")
    print("   PUT    /me             - Update personal info")
    print("   GET    /hobbies        - List all hobbies")
    print("   GET    /hobbies/{id}   - Get specific hobby")
    print("   POST   /hobbies        - Create new hobby")
    print("   PUT    /hobbies/{id}   - Update hobby")
    print("   DELETE /hobbies/{id}   - Delete hobby")
    print("   GET    /stats          - Get statistics")
    print()
    print("💡 Try filtering hobbies:")
    print("   GET /hobbies?skill_level=intermediate")
    print("   GET /hobbies?min_experience=2")
    print()
    print("="*60)
    
    # Run the server with hot reload for development
    uvicorn.run(
        "breakout03:app",  # Module:app_instance
        host="0.0.0.0",    # Listen on all network interfaces
        port=8000,          # Default port
        reload=True,        # Auto-reload on code changes (development only)
        log_level="info"    # Logging level
    )
