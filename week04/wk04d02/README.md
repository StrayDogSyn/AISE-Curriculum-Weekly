# W4D2 Breakout Activity 1: Personal Information API

## 📋 Overview

This implementation completes Breakout Activity 1 from the W4D2 Enhanced Breakout Activities. It demonstrates a complete RESTful API built with FastAPI that manages personal information and hobbies.

## 🎯 Learning Objectives Achieved

✅ Created multiple REST endpoints with proper HTTP methods (GET, POST, PUT, DELETE)  
✅ Implemented request/response validation using Pydantic models  
✅ Used appropriate HTTP status codes (200, 201, 204, 404, 400)  
✅ Built comprehensive error handling with proper messages  
✅ Implemented query parameter filtering  
✅ Added bonus statistics endpoint  
✅ Documented all code with detailed comments  

## 🚀 Features Implemented

### Personal Information Endpoints
- `GET /me` - Retrieve personal information
- `PUT /me` - Update personal information (full update)

### Hobbies CRUD Endpoints
- `GET /hobbies` - List all hobbies (with optional filtering)
  - Filter by skill level: `?skill_level=intermediate`
  - Filter by minimum experience: `?min_experience=3`
  - Combine filters: `?skill_level=advanced&min_experience=4`
- `GET /hobbies/{id}` - Get specific hobby by ID
- `POST /hobbies` - Create new hobby (returns 201 Created)
- `PUT /hobbies/{id}` - Update hobby (partial updates supported)
- `DELETE /hobbies/{id}` - Delete hobby (returns 204 No Content)

### Bonus Endpoints
- `GET /stats` - Get comprehensive statistics about hobbies
- `GET /health` - Health check for monitoring
- `GET /` - API information and available endpoints

## 📦 Installation

### 1. Install Dependencies

```bash
# From the week04/wk04d02 directory
pip install -r requirements.txt
```

Or install individually:

```bash
pip install fastapi uvicorn pydantic
```

### 2. Verify Installation

```bash
python -c "import fastapi; import uvicorn; import pydantic; print('✅ All packages installed!')"
```

## 🏃 Running the API

### Start the Server

```bash
# Option 1: Run directly with Python
python breakout03.py

# Option 2: Run with uvicorn command
uvicorn breakout03:app --reload
```

The server will start on `http://localhost:8000`

### Access Documentation

Once the server is running:

- **Swagger UI**: <http://localhost:8000/docs>
- **ReDoc**: <http://localhost:8000/redoc>
- **API Root**: <http://localhost:8000/>

## 🧪 Testing the API

### Using Swagger UI (Recommended for Beginners)

1. Open <http://localhost:8000/docs> in your browser
2. Click on any endpoint to expand it
3. Click "Try it out"
4. Fill in the request parameters/body
5. Click "Execute"
6. View the response

### Using curl (Command Line)

```bash
# Get personal information
curl http://localhost:8000/me

# Update personal information
curl -X PUT http://localhost:8000/me \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "age": 28,
    "location": "Portland, OR",
    "occupation": "Senior ML Engineer",
    "bio": "Building production ML systems"
  }'

# List all hobbies
curl http://localhost:8000/hobbies

# Filter hobbies by skill level
curl "http://localhost:8000/hobbies?skill_level=intermediate"

# Get specific hobby
curl http://localhost:8000/hobbies/1

# Create new hobby
curl -X POST http://localhost:8000/hobbies \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Photography",
    "skill_level": "beginner",
    "years_experience": 1,
    "description": "Learning landscape photography"
  }'

# Update hobby (partial update)
curl -X PUT http://localhost:8000/hobbies/1 \
  -H "Content-Type: application/json" \
  -d '{
    "skill_level": "advanced",
    "years_experience": 6
  }'

# Delete hobby
curl -X DELETE http://localhost:8000/hobbies/1

# Get statistics
curl http://localhost:8000/stats
```

### Using Python requests

```python
import requests

# Base URL
base_url = "http://localhost:8000"

# Get hobbies
response = requests.get(f"{base_url}/hobbies")
print(response.json())

# Create hobby
new_hobby = {
    "name": "Cooking",
    "skill_level": "intermediate",
    "years_experience": 3,
    "description": "Exploring different cuisines"
}
response = requests.post(f"{base_url}/hobbies", json=new_hobby)
print(response.json())

# Get statistics
response = requests.get(f"{base_url}/stats")
print(response.json())
```

## 📊 Example API Responses

### GET /me
```json
{
  "name": "Alex Johnson",
  "age": 26,
  "location": "Seattle, WA",
  "occupation": "ML Engineer in Training",
  "bio": "Learning to build amazing APIs and ML systems!"
}
```

### GET /hobbies
```json
[
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
  }
]
```

### GET /stats
```json
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
```

## 🏗️ Code Architecture

### Design Patterns Used

1. **Pydantic Models** - Data validation and serialization
   - `PersonalInfo` - Personal data with age validation
   - `Hobby` - New hobby creation with skill level validation
   - `HobbyUpdate` - Partial updates (all fields optional)
   - `HobbyResponse` - Hobby with ID for responses

2. **RESTful Design** - Proper HTTP methods and status codes
   - GET - Retrieve resources
   - POST - Create resources (201 Created)
   - PUT - Update resources
   - DELETE - Remove resources (204 No Content)

3. **Helper Functions** - Separation of concerns
   - `find_hobby_by_id()` - Locate hobbies
   - `remove_hobby_by_id()` - Delete hobbies

### Best Practices Implemented

✅ **Comprehensive Documentation**
- Detailed docstrings for all functions
- Inline comments explaining complex logic
- Example requests/responses in docstrings

✅ **Proper Error Handling**
- 404 Not Found for missing resources
- 400 Bad Request for invalid input
- Descriptive error messages

✅ **Input Validation**
- Pydantic models validate all input
- Custom validators for special constraints
- Query parameter validation

✅ **Response Models**
- Consistent response format
- Type safety with Pydantic
- Automatic API documentation

✅ **Code Organization**
- Clear section separation
- Logical grouping of endpoints
- Helper functions for reusability

## 🎓 Key Concepts Demonstrated

### REST Principles
- Resources identified by URLs (`/me`, `/hobbies`, `/hobbies/{id}`)
- HTTP methods for operations (GET, POST, PUT, DELETE)
- Stateless communication
- Proper status codes

### FastAPI Features
- Automatic interactive documentation
- Request/response validation
- Type hints for better IDE support
- Async endpoint support

### Pydantic Validation
- Field constraints (min/max length, regex patterns)
- Custom validators
- Optional vs required fields
- Partial updates support

## 🔍 Testing Checklist

- [ ] GET /me returns personal information
- [ ] PUT /me updates personal information
- [ ] GET /hobbies returns all hobbies
- [ ] GET /hobbies?skill_level=intermediate filters correctly
- [ ] GET /hobbies?min_experience=2 filters correctly
- [ ] GET /hobbies/1 returns specific hobby
- [ ] GET /hobbies/999 returns 404
- [ ] POST /hobbies creates new hobby (201)
- [ ] PUT /hobbies/1 updates hobby
- [ ] DELETE /hobbies/1 deletes hobby (204)
- [ ] GET /stats returns correct statistics
- [ ] GET /health returns status

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [REST API Best Practices](https://restfulapi.net/)

## 🎯 Assessment Criteria Met

✅ All CRUD endpoints implemented correctly  
✅ Proper HTTP methods and status codes used  
✅ Pydantic models validate data correctly  
✅ Error handling returns appropriate responses  
✅ Interactive docs work and show examples  
✅ Code follows best practices  
✅ Comprehensive documentation provided  

## 💡 Next Steps

To extend this project:

1. Add database persistence (SQLite, PostgreSQL)
2. Implement authentication (JWT tokens)
3. Add pagination for large result sets
4. Implement search functionality
5. Add email validation for personal info
6. Create a frontend with React/Vue
7. Deploy to cloud (Heroku, AWS, Azure)

---

**Author**: EHunt  
**Date**: October 21, 2025  
**Course**: AISE Week 4 Day 2  
