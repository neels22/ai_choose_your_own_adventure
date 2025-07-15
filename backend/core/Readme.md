# Core Package Documentation

This document provides comprehensive documentation for the core package, with detailed explanations of each component's purpose, functionality, and usage.

## Table of Contents
- [Configuration Setup](#configuration-setup)
- [Environment Variables](#environment-variables)
- [Field Validators](#field-validators)
- [Usage Examples](#usage-examples)
- [Best Practices](#best-practices)

---

## Configuration Setup

### Purpose and Overview

The `config.py` file serves as the central configuration management system for the entire project. Its primary purpose is to:

- **Map environment variables to Python objects** for easy access throughout the project
- **Provide type safety** and validation for configuration values
- **Centralize all configuration settings** in one location
- **Enable automatic loading** of settings from environment files

### File Structure

```python
# mapping env variables and to python object so that using it through entire project is easy

from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    DATABASE_URL: str 
    ALLOWED_ORIGINS: str = ""
    OPENAI_API_KEY: str 

    @field_validator('ALLOWED_ORIGINS')
    def parse_allowed_origins(cls, v: str) -> List[str]:
        return v.split(",") if v else []
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()
```

---

## Environment Variables

### What is the purpose and working of this config file?

The config file acts as a **bridge between environment variables and Python objects**. It:

1. **Automatically loads** environment variables from `.env` files
2. **Validates and converts** values to appropriate Python types
3. **Provides a centralized interface** for accessing configuration
4. **Ensures type safety** through Pydantic validation

### Meaning of Each Code Line

#### Imports
```python
from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator
```

- `typing.List`: Provides type hints for list operations
- `pydantic_settings.BaseSettings`: Base class that handles environment variable loading
- `pydantic.field_validator`: Decorator for custom field validation

#### Settings Class Definition
```python
class Settings(BaseSettings):
```

- **Purpose**: Defines the configuration schema
- **Inheritance**: Extends `BaseSettings` to get automatic env variable loading
- **Usage**: Creates a structured way to access all configuration values

#### Configuration Fields

| Field | Type | Default | Required | Purpose |
|-------|------|---------|----------|---------|
| `API_PREFIX` | `str` | `"/api"` | No | Base URL prefix for API endpoints |
| `DEBUG` | `bool` | `False` | No | Enables debug mode for development |
| `DATABASE_URL` | `str` | None | **Yes** | Database connection string |
| `ALLOWED_ORIGINS` | `str` | `""` | No | CORS allowed origins (comma-separated) |
| `OPENAI_API_KEY` | `str` | None | **Yes** | OpenAI API authentication key |

### What is class Config?

The `Config` class is a **Pydantic configuration class** that defines how the Settings class should behave:

```python
class Config:
    env_file = ".env"           # Specifies the environment file to load
    env_file_encoding = "utf-8" # Sets file encoding for reading
    case_sensitive = True       # Makes field names case-sensitive
```

**Purpose of each field:**
- `env_file`: Tells Pydantic which file to read environment variables from
- `env_file_encoding`: Ensures proper character encoding when reading the file
- `case_sensitive`: Maintains exact case matching for environment variable names

---

## Field Validators

### What is field validator?

A **field validator** is a Pydantic decorator that allows you to **transform and validate** field values before they're stored in the settings object.

### ALLOWED_ORIGINS Validator

```python
@field_validator('ALLOWED_ORIGINS')
def parse_allowed_origins(cls, v: str) -> List[str]:
    return v.split(",") if v else []
```

**What it does:**
1. **Takes a string** of comma-separated origins (e.g., "http://localhost:3000,https://myapp.com")
2. **Splits the string** by commas to create a list
3. **Returns an empty list** if no origins are provided
4. **Converts the result** from `str` to `List[str]`

**Example transformation:**
- Input: `"http://localhost:3000,https://myapp.com"`
- Output: `["http://localhost:3000", "https://myapp.com"]`

---

## Usage Examples

### How to use the settings object?

```python
# In main.py or any other file
from core.config import settings

# Access configuration values
api_prefix = settings.API_PREFIX
debug_mode = settings.DEBUG
database_url = settings.DATABASE_URL
allowed_origins = settings.ALLOWED_ORIGINS  # Already converted to list
openai_key = settings.OPENAI_API_KEY
```

### FastAPI Integration Example

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings

app = FastAPI()

# Use settings for CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # Already a list!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Environment File Setup

### Required .env File Structure

Create a `.env` file in your project root with these variables:

```env
# API Configuration
API_PREFIX=/api
DEBUG=true

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,https://myapp.com

# External API Keys
OPENAI_API_KEY=your_openai_api_key_here
```

### Automatic Loading Process

1. **Pydantic automatically reads** the `.env` file when `Settings()` is instantiated
2. **Environment variables are mapped** to the corresponding class fields
3. **Field validators are applied** to transform values as needed
4. **Type validation occurs** to ensure data integrity
5. **Settings object is created** with all validated values

---

## Error Handling

### Missing Required Fields

If a required field (like `DATABASE_URL` or `OPENAI_API_KEY`) is missing from the environment:

```python
# This will raise a ValidationError
settings = Settings()  # Error if DATABASE_URL not in .env
```

### Invalid Field Values

If a field contains invalid data (e.g., `DEBUG=not_a_boolean`):

```python
# This will raise a ValidationError with details
settings = Settings()
```

---

## Best Practices

### 1. Environment Variable Naming
- Use **UPPERCASE** for environment variables
- Use **underscores** to separate words
- Keep names **descriptive** and **clear**

### 2. Default Values
- Provide **sensible defaults** for non-critical settings
- Leave **required fields** without defaults to force explicit configuration

### 3. Validation
- Use **field validators** for complex transformations
- Implement **custom validation logic** for business rules
- Always **handle edge cases** (empty strings, null values)

### 4. Security
- **Never commit** `.env` files to version control
- Use **environment-specific** configuration files
- **Validate sensitive** configuration values

---

## Troubleshooting

### Common Issues

1. **"ValidationError: field required"**
   - Solution: Add missing environment variable to `.env` file

2. **"FileNotFoundError: .env"**
   - Solution: Create `.env` file in project root directory

3. **"UnicodeDecodeError"**
   - Solution: Ensure `.env` file is saved with UTF-8 encoding

4. **"Case sensitivity issues"**
   - Solution: Match exact case between `.env` variables and Settings class fields

### Debug Mode

Enable debug mode to see detailed validation errors:

```python
# In your .env file
DEBUG=true
```

---

## Summary

The `config.py` file provides a **robust, type-safe, and centralized** way to manage application configuration. It leverages Pydantic's powerful validation system to ensure data integrity while providing a clean, intuitive interface for accessing configuration values throughout your application.

**Key Benefits:**
- ✅ **Automatic environment variable loading**
- ✅ **Type safety and validation**
- ✅ **Centralized configuration management**
- ✅ **Easy integration with FastAPI and other frameworks**
- ✅ **Custom field transformation and validation**
- ✅ **Clear error messages for configuration issues**


