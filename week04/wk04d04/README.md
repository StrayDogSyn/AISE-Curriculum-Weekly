# FastAPI Boilerplate with Custom Logger

A production-ready FastAPI boilerplate following Python best practices and industry standards, featuring a professional custom logging module.

## ✨ Features

- ✅ **FastAPI Framework**: Modern, fast web framework for building APIs
- ✅ **Custom Logger Module**: Professional logging with colors, rotation, and structured output
- ✅ **Pydantic Models**: Data validation using Pydantic v2
- ✅ **Type Hints**: Full type annotation coverage
- ✅ **API Versioning**: Structured endpoint versioning (`/api/v1/`)
- ✅ **CORS Support**: Configurable Cross-Origin Resource Sharing
- ✅ **Error Handling**: Centralized exception handling
- ✅ **Documentation**: Auto-generated OpenAPI/Swagger docs
- ✅ **Environment Config**: Settings management with pydantic-settings
- ✅ **Testing**: Complete test suite with pytest
- ✅ **Performance Tracking**: Execution time decorators

## 📁 Project Structure

```text
.
├── myServer.py          # Main FastAPI application
├── myLogger.py          # Custom logging module ⭐
├── config.py            # Configuration management
├── examples.py          # Extended examples and patterns
├── test_myServer.py     # Test suite
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore rules
├── README.md           # This file
└── EXERCISE.md         # Breakout exercise guide
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip or poetry for dependency management

### Installation

1. **Clone or navigate to the project directory**

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

### Running the Application

**Development mode** (with auto-reload):
```bash
python myServer.py
```

**Or using uvicorn directly**:
```bash
uvicorn myServer:app --reload --host 0.0.0.0 --port 8000
```

**Production mode**:
```bash
uvicorn myServer:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Root & Health

- `GET /` - Welcome message
- `GET /health` - Health check endpoint

### Items API (v1)

- `GET /api/v1/items/{item_id}` - Get item by ID
  - Query params: `q` (optional search query)
  
- `GET /api/v1/users/{user_id}/items/{item_id}` - Get user's item
  - Query params: 
    - `q` (optional search query)
    - `short` (boolean, includes short description)

## 📚 Documentation

- **[EXERCISE.md](EXERCISE.md)** - Step-by-step breakout exercise
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - FastAPI quick reference
- **[EXERCISE_CHECKLIST.md](EXERCISE_CHECKLIST.md)** - Learning checklist

## 🎨 Custom Logger Features

### Color-Coded Console Output

The custom logger provides beautiful, color-coded console output:

- 🔵 **DEBUG** - Cyan - Detailed information for debugging
- 🟢 **INFO** - Green - General informational messages  
- 🟡 **WARNING** - Yellow - Warning messages
- 🔴 **ERROR** - Red - Error messages
- 🟣 **CRITICAL** - Magenta - Critical failures

### File Rotation

Logs automatically rotate when files reach 10MB, keeping the 5 most recent files:

```text
logs/
├── app.log        # Current log file
├── app.log.1      # Previous rotation
├── app.log.2      # ...
├── app.log.3
└── app.log.4
```

### Performance Tracking

Use the `@log_execution_time` decorator to track function performance:

```python
from myLogger import log_execution_time

@log_execution_time
async def slow_operation():
    # Your code here
    pass
```

### Structured Logging

Add context to your logs with `LogContext`:

```python
from myLogger import LogContext, get_logger

logger = get_logger(__name__)

with LogContext(logger, request_id="abc-123", user_id=42):
    logger.info("Processing request")
# Output includes: [request_id=abc-123] [user_id=42]
```

## 🧪 Testing the Logger

Run the logger demo to see all features:

```bash
python myLogger.py
```

You'll see:
- Different log levels with colors
- Execution timing demonstration
- Context tracking example
- File logging confirmation

## 📖 Usage Examples

### Basic Logging

```python
from myLogger import get_logger

logger = get_logger(__name__)

logger.debug("Debugging info")
logger.info("General info")
logger.warning("Warning message")
logger.error("Error occurred")
logger.critical("Critical failure!")
```

### With Performance Tracking

```python
from myLogger import get_logger, log_execution_time

logger = get_logger(__name__)

@log_execution_time
async def fetch_data(user_id: int):
    logger.info(f"Fetching data for user {user_id}")
    # Your code here
    return data
```

### With Structured Context

```python
from myLogger import get_logger, LogContext

logger = get_logger(__name__)

@app.get("/api/v1/items/{item_id}")
async def get_item(item_id: int):
    with LogContext(logger, item_id=item_id):
        logger.info("Fetching item")
        # All logs in this block will include item_id
        return {"item_id": item_id}
```

## 🔧 Configuration

### Log Levels

Set the log level in `myLogger.py`:

```python
# In LoggerConfig class
DEFAULT_LEVEL = logging.DEBUG  # or INFO, WARNING, ERROR, CRITICAL
```

### Log File Location

Configure where logs are stored:

```python
# In LoggerConfig class
LOG_DIR = Path("logs")  # Change to your preferred directory
LOG_FILE = LOG_DIR / "app.log"
```

### File Rotation Settings

Adjust rotation parameters:

```python
# In LoggerConfig class
MAX_BYTES = 10 * 1024 * 1024  # 10 MB
BACKUP_COUNT = 5  # Keep 5 backup files
```

### JSON Logging (for production)

Enable JSON formatted logs for log aggregation systems:

```python
logger = setup_logger(__name__, json_format=True)
```

## API Documentation

Once the server is running, visit:

- **Swagger UI**: <http://localhost:8000/api/docs>
- **ReDoc**: <http://localhost:8000/api/redoc>
- **OpenAPI JSON**: <http://localhost:8000/api/openapi.json>

## Best Practices Implemented

### 1. **Type Hints**
All functions use proper type annotations for better IDE support and type checking.

### 2. **Pydantic Models**
Request/response validation with:
- Field validation
- Default values
- Example schemas
- Documentation strings

### 3. **Async/Await**
Endpoints use `async def` for better concurrency (ready for async operations).

### 4. **Error Handling**
- Custom exception handlers
- Structured error responses
- HTTP status codes
- Logging of errors

### 5. **Documentation**
- Docstrings for all functions
- OpenAPI metadata
- Response models
- Tags for endpoint organization

### 6. **Configuration**
- Environment-based settings
- Pydantic settings validation
- Separate config module

### 7. **CORS**
- Configurable middleware
- Ready for frontend integration

### 8. **Logging**
- Structured logging
- Configurable log levels
- Request/error tracking

## Development Tips

### Testing Endpoints

Using curl:
```bash
# Root endpoint
curl http://localhost:8000/

# Health check
curl http://localhost:8000/health

# Get item
curl http://localhost:8000/api/v1/items/42?q=search

# Get user item
curl http://localhost:8000/api/v1/users/1/items/42?short=true
```

Using Python requests:
```python
import requests

response = requests.get("http://localhost:8000/api/v1/items/42")
print(response.json())
```

### Adding New Endpoints

1. Create a Pydantic model for request/response
2. Add the endpoint function with proper decorators
3. Include type hints and documentation
4. Add to appropriate tags for organization

Example:
```python
@app.post("/api/v1/items", response_model=Item, tags=["Items"])
async def create_item(item: Item) -> Item:
    """Create a new item."""
    # Your logic here
    return item
```

## Next Steps

### For Learning/Practice

- Add more endpoints (POST, PUT, DELETE)
- Implement database integration (SQLAlchemy)
- Add authentication (JWT tokens)
- Write tests (pytest)
- Add request validation
- Implement pagination

### For Production

- Set up proper logging (structured logging)
- Add rate limiting
- Implement caching (Redis)
- Add monitoring (Prometheus/Grafana)
- Use environment-specific configs
- Set up CI/CD pipeline
- Add database migrations (Alembic)
- Implement proper error tracking (Sentry)

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Uvicorn Documentation](https://www.uvicorn.org/)

## License

MIT License - Feel free to use this boilerplate for learning and projects!
