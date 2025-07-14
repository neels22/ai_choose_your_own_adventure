# AI Choose Your Own Adventure - Backend Project Structure

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Initial Setup](#initial-setup)
- [Dependencies](#dependencies)
- [Project Structure](#project-structure)
- [Package Organization](#package-organization)
- [File Descriptions](#file-descriptions)

## 🎯 Project Overview

This document outlines the complete setup and structure of the backend for the AI Choose Your Own Adventure application. The backend is built using FastAPI with modern Python practices, including proper package organization and dependency management.

## 🚀 Initial Setup

### Step 1: Project Initialization
```bash
uv init .
```

**Purpose**: The `uv init` command is a modern Python project initialization tool that:
- Creates a `.venv` directory and sets up a Python virtual environment
- Initializes a basic `pyproject.toml` with project metadata
- Optionally adds dependencies interactively
- Provides a clean, modern alternative to traditional `pip` and `venv` workflows

### Step 2: Generated Files
After initialization, the following files are created:

| File | Purpose | Description |
|------|---------|-------------|
| `pyproject.toml` | Project configuration | Modern Python project configuration file containing name, version, dependencies, and build settings |
| `uv.lock` | Dependency lock file | Similar to `package-lock.json`, ensures consistent package versions across environments |
| `main.py` | Entry point | Main project file that serves as the application's entry point |
| `.venv/` | Virtual environment | Isolated Python environment for project dependencies |

## 📦 Dependencies

### Step 3: Adding Core Dependencies
```bash
uv add 'fastapi[all]' langchain langchain-openai python-dotenv sqlalchemy uvicorn psycopg2-binary
```

**Purpose**: This command installs all necessary dependencies into the virtual environment.

### Dependency Breakdown

| Package | Version | Purpose |
|---------|---------|---------|
| **fastapi[all]** | ≥0.116.1 | Modern, high-performance web framework for building APIs with Python. The `[all]` includes optional dependencies like `uvicorn`, `pydantic`, and `httpx` for full async support |
| **langchain** | ≥0.3.26 | Framework for building applications powered by language models; enables chaining LLM calls and data sources |
| **langchain-openai** | ≥0.3.28 | OpenAI-specific integration for LangChain, used to access GPT models like ChatGPT or GPT-4 |
| **python-dotenv** | ≥1.1.1 | Loads environment variables from a `.env` file into Python, useful for managing API keys and secrets securely |
| **sqlalchemy** | ≥2.0.41 | SQL toolkit and ORM for Python, used for defining models and interacting with databases |
| **uvicorn** | ≥0.35.0 | ASGI server to run FastAPI applications in production or development |
| **psycopg2-binary** | ≥2.9.10 | PostgreSQL database adapter for Python, used to connect SQLAlchemy with a PostgreSQL database |

## 🏗️ Project Structure

### Step 4: Creating Package Structure

The backend follows a modular architecture with clear separation of concerns:

```
backend/
├── __init__.py              # Marks backend as a Python package
├── main.py                  # Application entry point
├── pyproject.toml          # Project configuration
├── uv.lock                 # Dependency lock file
├── .venv/                  # Virtual environment
├── core/                   # Application logic and main operations
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   ├── models.py           # Core business models
│   ├── prompts.py          # AI prompt templates
│   └── story_generator.py  # Story generation logic
├── db/                     # Database operations
│   ├── __init__.py
│   └── database.py         # Database connection and setup
├── models/                 # Database models (SQLAlchemy ORM)
│   ├── __init__.py
│   ├── job_model.py        # Job-related database models
│   └── story_model.py      # Story-related database models
├── routers/                # API route handlers
│   ├── __init__.py
│   ├── job_router.py       # Job-related API endpoints
│   └── story_router.py     # Story-related API endpoints
└── schemas/                # Data validation schemas
    ├── __init__.py
    ├── job_schema.py       # Job-related data schemas
    └── story_schema.py     # Story-related data schemas
```

## 📦 Package Organization

### Step 5: Creating Python Packages

Each directory is converted into a Python package using `__init__.py` files:

#### **`__init__.py` Files**
**Purpose**: Marks directories as Python packages, enabling:
- Clean module organization and imports
- Relative or absolute imports like `from backend.routers import job_router`
- Package-level initialization code execution
- Test discovery and IDE features

**Why it's important in modern Python**:
- Python 3.3+ supports implicit namespace packages without `__init__.py`
- However, adding `__init__.py` is still recommended for:
  - Maintain compatibility
  - Improve code clarity
  - Enable test discovery and IDE features

## 📁 File Descriptions

### Core Package (`core/`)
**Purpose**: Contains the main application logic and business operations

| File | Purpose |
|------|---------|
| `config.py` | Configuration management for environment variables, API keys, and application settings |
| `models.py` | Core business models and data structures used throughout the application |
| `prompts.py` | AI prompt templates and configurations for story generation |
| `story_generator.py` | Main logic for generating interactive stories using AI models |

### Database Package (`db/`)
**Purpose**: Handles all database-related operations and connections

| File | Purpose |
|------|---------|
| `database.py` | Database connection setup, session management, and SQLAlchemy engine configuration |

### Models Package (`models/`)
**Purpose**: Contains SQLAlchemy ORM models for database tables

| File | Purpose |
|------|---------|
| `job_model.py` | Database models for job-related entities (e.g., story generation jobs) |
| `story_model.py` | Database models for story-related entities (e.g., stories, chapters, choices) |

### Routers Package (`routers/`)
**Purpose**: Handles API route definitions and HTTP request processing

| File | Purpose |
|------|---------|
| `job_router.py` | API endpoints for job management (create, read, update, delete jobs) |
| `story_router.py` | API endpoints for story operations (generate, retrieve, update stories) |

### Schemas Package (`schemas/`)
**Purpose**: Defines data validation schemas for API input/output using Pydantic

| File | Purpose |
|------|---------|
| `job_schema.py` | Pydantic schemas for job-related data validation and serialization |
| `story_schema.py` | Pydantic schemas for story-related data validation and serialization |

## 🔧 Development Workflow

### Running the Application
```bash
# Activate virtual environment
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate     # On Windows

# Run the FastAPI application
uvicorn main:app --reload
```

### Adding New Dependencies
```bash
uv add package-name
```

### Updating Dependencies
```bash
uv sync
```

## 📝 Best Practices Implemented

1. **Modular Architecture**: Clear separation of concerns with dedicated packages
2. **Modern Python Tools**: Using `uv` for dependency management and virtual environments
3. **Type Safety**: Leveraging Pydantic schemas for data validation
4. **Async Support**: FastAPI with full async capabilities
5. **Database Abstraction**: SQLAlchemy ORM for database operations
6. **Environment Management**: Secure handling of configuration and secrets

## 🎯 Next Steps

1. Implement the core business logic in each module
2. Set up database migrations
3. Add authentication and authorization
4. Implement error handling and logging
5. Add comprehensive tests
6. Set up CI/CD pipeline

---

*This documentation provides a complete overview of the backend project structure, making it easy for developers to understand the architecture and contribute effectively.* 