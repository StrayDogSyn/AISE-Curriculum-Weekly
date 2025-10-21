# 🎯 W4D2 Enhanced Breakout Activities

## 📋 Overview
These breakout activities are designed to reinforce REST principles, FastAPI usage, and the integration of W4D1 design patterns with API development. Each activity includes clear learning objectives, starter code templates, and extension challenges.

---

## 🚀 Breakout Activity 1: Personal Information API (15 minutes)

### Learning Objectives
By completing this activity, you will:
- Create multiple REST endpoints with proper HTTP methods
- Implement request/response validation using Pydantic models
- Use appropriate HTTP status codes
- Test APIs using FastAPI's interactive documentation

### The Challenge
Build a **Personal Information API** that manages your profile, hobbies, and interests. This API will demonstrate all four core HTTP methods (GET, POST, PUT, DELETE) and proper data validation.

### Starter Code Template

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="Personal API",
    description="Manage personal information via REST API",
    version="1.0.0"
)

# ============================================
# PYDANTIC MODELS (Data Validation)
# ============================================

class PersonalInfo(BaseModel):
    """Personal information model"""
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=0, le=150)
    location: str
    occupation: str
    bio: Optional[str] = None
    
    @validator('age')
    def age_must_be_realistic(cls, v):
        if v < 0 or v > 150:
            raise ValueError('Age must be between 0 and 150')
        return v

class Hobby(BaseModel):
    """Hobby model with validation"""
    name: str = Field(..., min_length=1)
    skill_level: str = Field(..., regex="^(beginner|intermediate|advanced|expert)$")
    years_experience: int = Field(..., ge=0)
    description: Optional[str] = None
    
class HobbyUpdate(BaseModel):
    """Model for updating hobby (all fields optional)"""
    name: Optional[str] = None
    skill_level: Optional[str] = None
    years_experience: Optional[int] = None
    description: Optional[str] = None

# ============================================
# IN-MEMORY DATA STORAGE
# ============================================

# Your personal information (singleton-like data)
personal_info_db = {
    "name": "Your Name",
    "age": 25,
    "location": "Your City",
    "occupation": "ML Engineer in Training",
    "bio": "Learning to build amazing APIs!"
}

# Hobbies database (simulating storage)
hobbies_db: List[dict] = [
    {
        "id": 1,
        "name": "Programming",
        "skill_level": "intermediate",
        "years_experience": 2,
        "description": "Love building Python applications"
    },
    {
        "id": 2,
        "name": "Machine Learning",
        "skill_level": "beginner",
        "years_experience": 1,
        "description": "Exploring AI and data science"
    }
]

# Counter for hobby IDs
hobby_id_counter = 3

# ============================================
# TODO: IMPLEMENT THE API ENDPOINTS BELOW
# ============================================

# ENDPOINT 1: GET /me - Retrieve personal information
@app.get("/me", response_model=PersonalInfo)
async def get_personal_info():
    """
    Get your personal information.
    
    Returns:
        PersonalInfo: Your current personal information
    """
    # TODO: Return personal_info_db as PersonalInfo model
    pass


# ENDPOINT 2: PUT /me - Update personal information
@app.put("/me", response_model=PersonalInfo)
async def update_personal_info(info: PersonalInfo):
    """
    Update your personal information.
    
    Args:
        info: Updated personal information
        
    Returns:
        PersonalInfo: Updated personal information
    """
    # TODO: Update personal_info_db with new info
    # TODO: Return updated info
    pass


# ENDPOINT 3: GET /hobbies - List all hobbies
@app.get("/hobbies")
async def get_hobbies(
    skill_level: Optional[str] = None,
    min_experience: Optional[int] = None
):
    """
    Get list of hobbies with optional filtering.
    
    Args:
        skill_level: Filter by skill level (beginner/intermediate/advanced/expert)
        min_experience: Filter by minimum years of experience
        
    Returns:
        List of hobbies matching the criteria
    """
    # TODO: Filter hobbies_db based on query parameters
    # TODO: Return filtered list
    pass


# ENDPOINT 4: GET /hobbies/{hobby_id} - Get specific hobby
@app.get("/hobbies/{hobby_id}")
async def get_hobby(hobby_id: int):
    """
    Get details of a specific hobby.
    
    Args:
        hobby_id: ID of the hobby to retrieve
        
    Returns:
        Hobby details
        
    Raises:
        HTTPException 404: Hobby not found
    """
    # TODO: Find hobby by ID
    # TODO: Return 404 if not found
    # TODO: Return hobby if found
    pass


# ENDPOINT 5: POST /hobbies - Add new hobby
@app.post("/hobbies", status_code=status.HTTP_201_CREATED)
async def add_hobby(hobby: Hobby):
    """
    Add a new hobby to your collection.
    
    Args:
        hobby: New hobby information
        
    Returns:
        Created hobby with assigned ID
    """
    global hobby_id_counter
    
    # TODO: Create new hobby dict with ID
    # TODO: Add to hobbies_db
    # TODO: Increment hobby_id_counter
    # TODO: Return created hobby with 201 status
    pass


# ENDPOINT 6: PUT /hobbies/{hobby_id} - Update hobby
@app.put("/hobbies/{hobby_id}")
async def update_hobby(hobby_id: int, hobby_update: HobbyUpdate):
    """
    Update an existing hobby.
    
    Args:
        hobby_id: ID of hobby to update
        hobby_update: Fields to update
        
    Returns:
        Updated hobby
        
    Raises:
        HTTPException 404: Hobby not found
    """
    # TODO: Find hobby by ID (return 404 if not found)
    # TODO: Update only provided fields
    # TODO: Return updated hobby
    pass


# ENDPOINT 7: DELETE /hobbies/{hobby_id} - Delete hobby
@app.delete("/hobbies/{hobby_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hobby(hobby_id: int):
    """
    Delete a hobby from your collection.
    
    Args:
        hobby_id: ID of hobby to delete
        
    Raises:
        HTTPException 404: Hobby not found
    """
    # TODO: Find hobby by ID (return 404 if not found)
    # TODO: Remove from hobbies_db
    # TODO: Return 204 No Content
    pass


# BONUS ENDPOINT: GET /stats - Get statistics
@app.get("/stats")
async def get_stats():
    """
    Get statistics about your hobbies.
    
    Returns:
        Statistics including total hobbies, skill level distribution, etc.
    """
    # TODO: Calculate statistics from hobbies_db
    # - Total number of hobbies
    # - Average years of experience
    # - Distribution by skill level
    # - Most experienced hobby
    pass

# ============================================
# RUN THE SERVER
# ============================================

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Personal Information API...")
    print("📖 Documentation: http://localhost:8000/docs")
    print("🧪 Try creating, reading, updating, and deleting hobbies!")
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Testing Your ML API

1. **Test authentication**:

   ```bash
   # Should fail (no auth)
   curl http://localhost:8000/v1/models
   
   # Should succeed
   curl -H "Authorization: Bearer demo_key_123" \
        http://localhost:8000/v1/models
   ```

1. **Train a model**:

   ```bash
   curl -X POST http://localhost:8000/v1/models/train \
        -H "Authorization: Bearer demo_key_123" \
        -H "Content-Type: application/json" \
        -d '{
          "model_type": "random_forest",
          "dataset_name": "test_data",
          "training_strategy": "standard"
        }'
   ```

1. **Make predictions**:

   ```bash
   curl -X POST http://localhost:8000/v1/models/MODEL_ID/predict \
        -H "Authorization: Bearer demo_key_123" \
        -H "Content-Type: application/json" \
        -d '{
          "model_id": "MODEL_ID",
          "features": [[1.0, 2.0, 3.0, 4.0, 5.0]]
        }'
   ```

### Challenge Extensions

1. **Validation Enhancement**: Add more sophisticated validation
   - Email field with proper email validation
   - Phone number with format validation
   - Custom validators for specific fields

2. **Skills Endpoint**: Add a `/skills` resource
   - GET /skills - List programming languages you know
   - POST /skills - Add a new skill
   - Include proficiency level

3. **Search Functionality**: Add search endpoint
   - GET /search?q=python - Search across all fields
   - Return matching hobbies and skills

4. **Pagination**: Implement pagination for hobbies
   - GET /hobbies?page=1&limit=10
   - Return page metadata

---

## 🤖 Breakout Activity 2: ML API System Integration (15 minutes)

### Learning Objectives (Activity 2)
By completing this activity, you will:
- Integrate W4D1 design patterns with FastAPI endpoints
- Build a production-ready ML model API
- Implement authentication and authorization
- Create comprehensive error handling
- Design versioned API endpoints

### The Challenge (Activity 2)
Build a complete **ML Model API System** that:
- Uses Factory pattern to create different model types
- Uses Strategy pattern for different training approaches
- Uses Observer pattern for monitoring
- Uses Singleton pattern for configuration
- Includes authentication and proper error handling

### System Architecture

```text
┌─────────────────────────────────────────────────┐
│           FastAPI Application                    │
│                                                  │
│  ┌────────────┐  ┌─────────────┐  ┌──────────┐ │
│  │   Auth     │  │  Versioned  │  │  Error   │ │
│  │ Middleware │→ │  Endpoints  │→ │ Handlers │ │
│  └────────────┘  └─────────────┘  └──────────┘ │
│                         ↓                        │
│  ┌──────────────────────────────────────────┐  │
│  │       Design Patterns Layer              │  │
│  │  • Factory  • Strategy                   │  │
│  │  • Observer • Singleton                  │  │
│  └──────────────────────────────────────────┘  │
│                         ↓                        │
│  ┌──────────────────────────────────────────┐  │
│  │          ML Models                       │  │
│  │  Random Forest | SVM | Neural Network   │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

### Starter Code Template (Activity 2)

```python
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
import numpy as np
from enum import Enum

# Import your W4D1 design patterns
# Adjust these imports based on your W4D1 implementation
"""
from w4d1_patterns import (
    MLModelFactory,
    MLModelTrainer,
    StandardTrainingStrategy,
    CrossValidationStrategy,
    MonitoredMLModel,
    ConfigurationManager
)
"""

app = FastAPI(
    title="Production ML API",
    description="ML system with design patterns and professional features",
    version="2.0.0"
)

# ============================================
# ENUMS AND CONSTANTS
# ============================================

class ModelType(str, Enum):
    RANDOM_FOREST = "random_forest"
    SVM = "svm"
    NEURAL_NETWORK = "neural_network"

class TrainingStrategy(str, Enum):
    STANDARD = "standard"
    CROSS_VALIDATION = "cross_validation"

# ============================================
# PYDANTIC MODELS
# ============================================

class TrainingRequest(BaseModel):
    """Request model for training ML models"""
    model_type: ModelType = Field(..., description="Type of ML model")
    dataset_name: str = Field(..., min_length=1)
    hyperparameters: Optional[Dict[str, Any]] = Field(default_factory=dict)
    training_strategy: TrainingStrategy = Field(default=TrainingStrategy.STANDARD)

class TrainingResponse(BaseModel):
    """Response model for training results"""
    model_id: str
    model_type: ModelType
    training_accuracy: float
    training_time: float
    status: str
    created_at: datetime

class PredictionRequest(BaseModel):
    """Request model for predictions"""
    model_id: str
    features: List[List[float]] = Field(..., description="Feature vectors")

class PredictionResponse(BaseModel):
    """Response model for predictions"""
    model_id: str
    predictions: List[int]
    confidence_scores: Optional[List[float]] = None
    prediction_count: int
    timestamp: datetime

class ModelInfo(BaseModel):
    """Model information response"""
    model_id: str
    model_type: ModelType
    status: str
    training_accuracy: Optional[float]
    created_at: datetime
    last_used: Optional[datetime]
    prediction_count: int

# ============================================
# AUTHENTICATION
# ============================================

security = HTTPBearer()

# Simple API key authentication (in production, use proper JWT)
API_KEYS = {
    "demo_key_123": {"username": "demo_user", "permissions": ["read", "write"]},
    "admin_key_456": {"username": "admin", "permissions": ["read", "write", "admin"]}
}

class UserInfo(BaseModel):
    username: str
    permissions: List[str]

def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserInfo:
    """
    Verify API key from Authorization header.
    
    Raises:
        HTTPException 401: Invalid API key
    """
    api_key = credentials.credentials
    
    if api_key not in API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    user_data = API_KEYS[api_key]
    return UserInfo(**user_data)

def require_permission(permission: str):
    """Dependency to require specific permission"""
    def permission_checker(user: UserInfo = Depends(verify_api_key)):
        if permission not in user.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission}' required"
            )
        return user
    return permission_checker

# ============================================
# GLOBAL STATE (In production, use database)
# ============================================

# Trained models storage
trained_models: Dict[str, Any] = {}  # model_id -> MonitoredMLModel
model_metadata: Dict[str, Dict] = {}  # model_id -> metadata

# Configuration (Singleton pattern from W4D1)
# config = ConfigurationManager()

# ============================================
# TODO: IMPLEMENT API ENDPOINTS
# ============================================

# ENDPOINT 1: Health check (public, no auth)
@app.get("/health")
async def health_check():
    """
    Check API health status.
    No authentication required.
    """
    # TODO: Return health status
    # - API status
    # - Number of active models
    # - Timestamp
    pass


# ENDPOINT 2: Train model (requires 'write' permission)
@app.post("/v1/models/train", response_model=TrainingResponse)
async def train_model_v1(
    request: TrainingRequest,
    user: UserInfo = Depends(require_permission("write"))
):
    """
    Train a new ML model using Factory and Strategy patterns.
    
    Design Patterns Used:
    - Factory: Create different model types
    - Strategy: Different training approaches
    - Observer: Monitor training progress
    
    Requires: 'write' permission
    """
    # TODO: Implement training logic
    # 1. Use Factory to create model based on request.model_type
    # 2. Wrap with Observer (MonitoredMLModel)
    # 3. Use Strategy pattern for training approach
    # 4. Store trained model in trained_models dict
    # 5. Store metadata in model_metadata dict
    # 6. Return TrainingResponse
    pass


# ENDPOINT 3: Make predictions (requires 'read' permission)
@app.post("/v1/models/{model_id}/predict", response_model=PredictionResponse)
async def make_predictions_v1(
    model_id: str,
    request: PredictionRequest,
    user: UserInfo = Depends(require_permission("read"))
):
    """
    Make predictions using a trained model.
    
    Observer pattern automatically logs predictions.
    
    Requires: 'read' permission
    """
    # TODO: Implement prediction logic
    # 1. Verify model exists (404 if not)
    # 2. Verify model_id matches request (400 if mismatch)
    # 3. Convert features to numpy array
    # 4. Make predictions (Observer logs automatically)
    # 5. Update model metadata (last_used, prediction_count)
    # 6. Return PredictionResponse
    pass


# ENDPOINT 4: List models (requires 'read' permission)
@app.get("/v1/models", response_model=List[ModelInfo])
async def list_models_v1(
    user: UserInfo = Depends(require_permission("read"))
):
    """
    List all trained models.
    
    Requires: 'read' permission
    """
    # TODO: Return list of ModelInfo for all models
    pass


# ENDPOINT 5: Get model info (requires 'read' permission)
@app.get("/v1/models/{model_id}", response_model=ModelInfo)
async def get_model_info_v1(
    model_id: str,
    user: UserInfo = Depends(require_permission("read"))
):
    """
    Get detailed information about a specific model.
    
    Requires: 'read' permission
    """
    # TODO: Return ModelInfo for specific model (404 if not found)
    pass


# ENDPOINT 6: Delete model (requires 'admin' permission)
@app.delete("/v1/models/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_model_v1(
    model_id: str,
    user: UserInfo = Depends(require_permission("admin"))
):
    """
    Delete a trained model.
    
    Requires: 'admin' permission
    """
    # TODO: Remove model from storage (404 if not found)
    # Return 204 No Content
    pass


# ENDPOINT 7: Get model metrics (requires 'read' permission)
@app.get("/v1/models/{model_id}/metrics")
async def get_model_metrics_v1(
    model_id: str,
    user: UserInfo = Depends(require_permission("read"))
):
    """
    Get performance metrics for a model.
    
    Observer pattern tracks these automatically.
    """
    # TODO: Return metrics from Observer
    # - Total predictions made
    # - Average prediction time
    # - Accuracy over time
    # - Recent predictions
    pass


# ENDPOINT 8: Get API metrics (requires 'admin' permission)
@app.get("/admin/metrics")
async def get_api_metrics(
    user: UserInfo = Depends(require_permission("admin"))
):
    """
    Get overall API usage metrics.
    
    Requires: 'admin' permission
    """
    # TODO: Return API-wide metrics
    # - Total models trained
    # - Total predictions made
    # - Most used model
    # - Average model accuracy
    pass


# ENDPOINT 9: Version 2 endpoint example (backward compatible)
@app.get("/v2/models", response_model=List[ModelInfo])
async def list_models_v2(
    include_inactive: bool = False,
    user: UserInfo = Depends(require_permission("read"))
):
    """
    Version 2: List models with additional filtering options.
    
    Demonstrates API versioning for backward compatibility.
    """
    # TODO: Implement v2 with additional features
    # - Filter by active/inactive status
    # - Additional metadata
    pass

# ============================================
# ERROR HANDLERS
# ============================================

class MLAPIError(Exception):
    """Base exception for ML API errors"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class ModelNotFoundError(MLAPIError):
    """Raised when model doesn't exist"""
    def __init__(self, model_id: str):
        super().__init__(
            message=f"Model {model_id} not found",
            status_code=404
        )

class ModelTrainingError(MLAPIError):
    """Raised when training fails"""
    def __init__(self, reason: str):
        super().__init__(
            message=f"Training failed: {reason}",
            status_code=422
        )

# TODO: Add exception handlers for custom errors
# @app.exception_handler(ModelNotFoundError)
# async def model_not_found_handler(request, exc: ModelNotFoundError):
#     return JSONResponse(...)

# ============================================
# RUN SERVER
# ============================================

if __name__ == "__main__":
    import uvicorn
    print("🤖 Starting Production ML API...")
    print("📖 Docs: http://localhost:8000/docs")
    print("🔑 Test with API key: demo_key_123")
    print("\nExample curl commands:")
    print('  curl -H "Authorization: Bearer demo_key_123" http://localhost:8000/v1/models')
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Testing Your ML API (Activity 2)

1. **Test authentication**:

   ```bash
   # Should fail (no auth)
   curl http://localhost:8000/v1/models
   
   # Should succeed
   curl -H "Authorization: Bearer demo_key_123" \
        http://localhost:8000/v1/models
   ```

1. **Train a model**:

   ```bash
   curl -X POST http://localhost:8000/v1/models/train \
        -H "Authorization: Bearer demo_key_123" \
        -H "Content-Type: application/json" \
        -d '{
          "model_type": "random_forest",
          "dataset_name": "test_data",
          "training_strategy": "standard"
        }'
   ```

1. **Make predictions**:

   ```bash
   curl -X POST http://localhost:8000/v1/models/MODEL_ID/predict \
        -H "Authorization: Bearer demo_key_123" \
        -H "Content-Type: application/json" \
        -d '{
          "model_id": "MODEL_ID",
          "features": [[1.0, 2.0, 3.0, 4.0, 5.0]]
        }'
   ```

### Challenge Extensions (Activity 2)

1. **Rate Limiting**: Implement request rate limiting
   - Track requests per user
   - Return 429 when limit exceeded

2. **Async Training**: Make training async with task tracking
   - POST /v1/models/train-async returns task_id
   - GET /v1/tasks/{task_id} checks status

3. **Model Versioning**: Support multiple versions of same model
   - POST /v1/models/{model_id}/versions
   - GET /v1/models/{model_id}/versions

4. **Caching**: Add caching for predictions
   - Cache frequently-used predictions
   - Reduce computation time

5. **WebSockets**: Add real-time training updates
   - Stream training progress via WebSocket
   - Live accuracy updates

---

## 📊 Assessment Criteria

### Breakout 1 Assessment
- ✅ All CRUD endpoints implemented correctly
- ✅ Proper HTTP methods and status codes used
- ✅ Pydantic models validate data correctly
- ✅ Error handling returns appropriate responses
- ✅ Interactive docs work and show examples

### Breakout 2 Assessment
- ✅ W4D1 patterns integrated with API endpoints
- ✅ Authentication protects endpoints correctly
- ✅ Different permission levels work as expected
- ✅ Error handling is comprehensive
- ✅ API versioning demonstrates backward compatibility

---

## 💡 Tips for Success

1. **Test as you go**: Use `/docs` to test each endpoint immediately after implementing it

2. **Read error messages**: FastAPI provides excellent error messages - use them!

3. **Use type hints**: They enable automatic validation and documentation

4. **Think REST**: 
   - Resources are nouns (users, hobbies, models)
   - Actions are HTTP methods (GET, POST, PUT, DELETE)
   - Status codes communicate results

5. **Pattern thinking**:
   - Need to create different things? → Factory
   - Need to switch algorithms? → Strategy
   - Need to track events? → Observer
   - Need shared configuration? → Singleton

6. **Start simple**: Get basic endpoints working first, then add complexity

---

## 🎯 Learning Outcomes

After completing both breakouts, you will be able to:
- ✅ Design and implement RESTful APIs
- ✅ Use FastAPI for rapid API development
- ✅ Integrate design patterns with web APIs
- ✅ Implement authentication and authorization
- ✅ Handle errors gracefully with proper status codes
- ✅ Create self-documenting APIs
- ✅ Test APIs using interactive documentation
- ✅ Build production-ready ML APIs

**Remember**: These skills are exactly what companies like Spotify, Uber, and Netflix use to serve millions of users. You're learning industry-standard practices!
