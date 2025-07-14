# FastAPI Setup Documentation

## Overview
This document provides a comprehensive guide to the FastAPI setup for the "Choose Your Own Adventure" game backend. Each component is explained with its purpose and functionality.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Import Statements](#import-statements)
3. [FastAPI Application Configuration](#fastapi-application-configuration)
4. [CORS Middleware Setup](#cors-middleware-setup)
5. [Application Entry Point](#application-entry-point)
6. [Running the Application](#running-the-application)
7. [API Documentation](#api-documentation)

---

## Prerequisites

### Python Interpreter Setup
**Important**: Ensure you're using the correct Python interpreter to avoid import errors and squiggly lines in your IDE.

**Steps:**
1. Copy the path to your project's Python interpreter
2. In your IDE (VS Code, PyCharm, etc.), select the correct interpreter
3. This ensures all imports work correctly and eliminates import warnings

---

## Import Statements

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
```

### Purpose of Each Import:

1. **`FastAPI`**: The main web framework for building APIs with Python
   - Provides high performance, easy to use, and automatic API documentation
   - Based on Starlette and Pydantic

2. **`CORSMiddleware`**: Cross-Origin Resource Sharing middleware
   - Allows web applications to make requests to APIs hosted on different domains
   - Essential for frontend-backend communication

3. **`uvicorn`**: ASGI server implementation
   - Lightweight and fast ASGI server
   - Used to run the FastAPI application

---

## FastAPI Application Configuration

```python
app = FastAPI(
    title="Choose your own adventure",
    description="A simple choose your own adventure game",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)
```

### Configuration Parameters Explained:

1. **`title`**: The name of your API
   - Appears in the API documentation
   - Used in OpenAPI specification

2. **`description`**: Brief description of what your API does
   - Shown in the documentation pages
   - Helps other developers understand your API's purpose

3. **`version`**: Current version of your API
   - Follows semantic versioning (MAJOR.MINOR.PATCH)
   - Important for API versioning and documentation

4. **`docs_url="/docs"`**: URL path for Swagger UI documentation
   - Provides interactive API documentation
   - Accessible at `http://localhost:8000/docs`
   - Allows testing endpoints directly from the browser

5. **`redoc_url="/redoc"`**: URL path for ReDoc documentation
   - Alternative documentation interface
   - More visually appealing than Swagger UI
   - Accessible at `http://localhost:8000/redoc`

### What is ReDoc?
ReDoc is an alternative API documentation interface that provides:
- Clean, responsive design
- Better mobile experience
- Automatic code sample generation
- Search functionality
- Better handling of complex schemas

---

## CORS Middleware Setup

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### CORS Middleware Parameters Explained:

1. **`allow_origins=["*"]`**: 
   - **Purpose**: Controls which origins can access your API
   - **`["*"]`**: Allows all origins (domains) to access the API
   - **Production Note**: In production, replace `["*"]` with specific allowed origins like `["http://localhost:3000", "https://yourapp.com"]`

2. **`allow_credentials=True`**:
   - **Purpose**: Allows cookies and authentication headers to be sent with requests
   - **Use Case**: Required for session-based authentication or JWT tokens
   - **Security**: Only enable if your frontend needs to send credentials

3. **`allow_methods=["*"]`**:
   - **Purpose**: Specifies which HTTP methods are allowed
   - **`["*"]`**: Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
   - **Alternative**: Can specify specific methods like `["GET", "POST", "PUT"]`

4. **`allow_headers=["*"]`**:
   - **Purpose**: Controls which HTTP headers can be sent with requests
   - **`["*"]`**: Allows all headers
   - **Common Headers**: Authorization, Content-Type, Accept, etc.

### What Each CORS Parameter Means:
- **Origins**: The domains that can access your API
- **Credentials**: Whether authentication data can be sent
- **Methods**: Which HTTP operations are permitted
- **Headers**: Which request headers are allowed

---

## Application Entry Point

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

### Purpose of `__name__ == "__main__"`:
This Python idiom ensures the code block only runs when the script is executed directly, not when imported as a module.

**How it works:**
- When you run `python main.py`, `__name__` equals `"__main__"`
- When you import `main.py` from another file, `__name__` equals `"main"`
- This prevents the server from starting when the file is imported

### Uvicorn Run Parameters Explained:

1. **`"main:app"`**:
   - **Format**: `"filename:app_variable"`
   - **`main`**: The Python file name (without .py extension)
   - **`app`**: The FastAPI application instance variable name
   - **Purpose**: Tells uvicorn which application to run

2. **`host="0.0.0.0"`**:
   - **Purpose**: Binds the server to all available network interfaces
   - **`0.0.0.0`**: Accepts connections from any IP address
   - **Alternative**: `"127.0.0.1"` or `"localhost"` for local-only access
   - **Production**: Use `"0.0.0.0"` for external access

3. **`port=8000`**:
   - **Purpose**: The port number on which the server will listen
   - **Default**: FastAPI typically uses port 8000
   - **Alternative**: Can use any available port (3000, 5000, etc.)

4. **`reload=True`**:
   - **Purpose**: Automatically restarts the server when code changes are detected
   - **Development**: Essential for development workflow
   - **Production**: Should be `False` in production for performance
   - **Note**: Only works when running the file directly, not with `uvicorn` command

---

## Running the Application

### Command to Run FastAPI Application:
```bash
uv run main.py
```

### Alternative Commands:
```bash
# Using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Using python
python main.py

# Using uvicorn with different options
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### What Each Command Does:
- **`uv run main.py`**: Uses uv package manager to run the Python file
- **`uvicorn main:app`**: Directly runs the uvicorn server
- **`python main.py`**: Executes the Python file, triggering the `if __name__ == "__main__"` block

---

## API Documentation

Once the server is running, you can access:

1. **Swagger UI**: `http://localhost:8000/docs`
   - Interactive API documentation
   - Test endpoints directly
   - See request/response schemas

2. **ReDoc**: `http://localhost:8000/redoc`
   - Alternative documentation interface
   - Better for complex APIs
   - More visually appealing

3. **OpenAPI JSON**: `http://localhost:8000/openapi.json`
   - Raw OpenAPI specification
   - Used by documentation tools

---

## Development Workflow

1. **Start the server**: `uv run main.py`
2. **Make code changes**: Edit your Python files
3. **Auto-reload**: Server automatically restarts (thanks to `reload=True`)
4. **Test endpoints**: Use `/docs` or `/redoc` to test your API
5. **Monitor logs**: Check terminal for request logs and errors

---

## Security Considerations

### Development vs Production:

**Development Settings:**
- `allow_origins=["*"]` - OK for development
- `reload=True` - Useful for development
- `host="0.0.0.0"` - OK for local development

**Production Settings:**
- `allow_origins=["https://yourapp.com"]` - Specify exact origins
- `reload=False` - Disable auto-reload for performance
- Use environment variables for sensitive configuration
- Implement proper authentication and authorization

---

## Troubleshooting

### Common Issues:

1. **Port already in use**: Change port number or kill existing process
2. **Import errors**: Check Python interpreter and virtual environment
3. **CORS errors**: Verify middleware configuration
4. **Auto-reload not working**: Ensure `reload=True` and running file directly

### Debug Commands:
```bash
# Check if port is in use
lsof -i :8000

# Kill process on port 8000
kill -9 $(lsof -t -i:8000)

# Check Python environment
which python
python --version
```

---

## Next Steps

1. **Add Routes**: Create API endpoints in separate router files
2. **Database Integration**: Set up database models and connections
3. **Authentication**: Implement user authentication and authorization
4. **Testing**: Add unit tests and integration tests
5. **Deployment**: Configure for production deployment

This setup provides a solid foundation for building a scalable FastAPI application with proper documentation and development tools.

