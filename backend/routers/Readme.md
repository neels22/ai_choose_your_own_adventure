# Routers Documentation

This folder contains the route definitions for our AI Choose Your Own Adventure FastAPI application. Routers are where we define the API endpoints that clients will interact with.

## Table of Contents
- [What are Routers?](#what-are-routers)
- [APIRouter Explained](#apirouter-explained)
- [Core FastAPI Concepts](#core-fastapi-concepts)
- [Session Management](#session-management)
- [Story Router](#story-router)
- [Job Router](#job-router)
- [API Endpoints Summary](#api-endpoints-summary)
- [FAQ](#faq)

## What are Routers?

In FastAPI, **routers** are a way to organize your API endpoints into separate modules instead of putting everything in one large file. Think of routers as different sections of your API:

- `story_router.py` - Handles all story-related operations
- `job_router.py` - Handles job status checking

This modular approach makes your code:
- **Easier to maintain** - Related functionality is grouped together
- **More readable** - Smaller, focused files
- **Better organized** - Clear separation of concerns

## APIRouter Explained

### What is APIRouter?

`APIRouter` is a FastAPI class that allows you to create a group of related routes. Each router can have its own configuration.

```python
router = APIRouter(
    prefix="/stories",  # All routes will start with /stories
    tags=["stories"],   # Groups endpoints in API documentation
)
```

### Prefix
The `prefix` automatically prepends a path to all routes in this router:
- Without prefix: `@router.post("/create")` → `/create`
- With prefix `/stories`: `@router.post("/create")` → `/stories/create`

### Tags
The `tags` parameter groups related endpoints in the automatically generated API documentation (Swagger UI). All endpoints in this router will be grouped under the "stories" tag.

## Core FastAPI Concepts

### Depends
`Depends()` is FastAPI's dependency injection system. It automatically calls a function and provides its result to your endpoint:

```python
def get_db():
    # Returns a database session
    
@router.post("/create")
def create_story(db: Session = Depends(get_db)):
    # FastAPI automatically calls get_db() and passes the result as 'db'
```

### Cookie
`Cookie()` extracts values from HTTP cookies sent by the browser:

```python
def get_session_id(session_id: Optional[str] = Cookie(None)):
    # Extracts 'session_id' from browser cookies
    # If no cookie exists, session_id will be None
```

### Response
`Response` allows you to modify the HTTP response, such as setting cookies:

```python
def create_story(response: Response):
    response.set_cookie(key="session_id", value="abc123", httponly=True)
    # Sets a cookie that the browser will store and send back
```

### BackgroundTasks
`BackgroundTasks` lets you run functions after returning a response to the user:

```python
def create_story(background_tasks: BackgroundTasks):
    background_tasks.add_task(some_long_function)
    return {"message": "Started processing"}
    # User gets immediate response, then some_long_function runs
```

## Session Management

### What is a Session?
A **session** is a way to identify and remember a specific user's browser across multiple requests. Think of it like a temporary ID card that lets the server know "this request is from the same person who made a request 5 minutes ago."

### How Our Session System Works

1. **First Visit**: When a user first visits, they have no session ID
2. **Create Session**: We generate a unique UUID (like `abc123-def456-ghi789`)
3. **Store in Cookie**: We send this ID back to the browser as a cookie
4. **Future Requests**: Browser automatically sends the session ID with every request
5. **Identify User**: Server uses the session ID to know which user is making the request

```python
def get_session_id(session_id: Optional[str] = Cookie(None)):
    if not session_id:
        session_id = str(uuid.uuid4())  # Generate new UUID
    return session_id
```

### Why Use Sessions?
- **Track user progress** through stories
- **Associate jobs** with specific users
- **Maintain state** without requiring user login

## Story Router

The story router (`story_router.py`) handles all story-related operations.

### Endpoints

#### POST `/stories/create`
**Purpose**: Creates a new story generation job

**What happens**:
1. Gets or creates a session ID for the user
2. Stores the session ID in a browser cookie
3. Creates a new job in the database with status "pending"
4. Starts background task to generate the actual story
5. Returns job information immediately

**Parameters**:
- `request: CreateStoryRequest` - Contains the story theme
- `background_tasks: BackgroundTasks` - For running story generation
- `response: Response` - To set cookies
- `session_id: str` - User's session (auto-injected)
- `db: Session` - Database connection (auto-injected)

**Example Flow**:
```
User → POST /stories/create {"theme": "space adventure"}
     → Server creates job with ID "abc123"
     → Server returns {"job_id": "abc123", "status": "pending"}
     → Background: Server generates story content
```

#### GET `/stories/{story_id}/complete`
**Purpose**: Retrieves a complete story with all its nodes

**What happens**:
1. Looks up the story in the database by ID
2. Builds a complete story tree (all chapters and choices)
3. Returns the full story structure

**Parameters**:
- `story_id: int` - The ID of the story to retrieve
- `db: Session` - Database connection (auto-injected)

### Key Functions

#### `generate_story_task()`
This function runs in the background after a story creation request:

1. **Update Status**: Changes job status to "processing"
2. **Generate Content**: Creates the actual story (currently TODO)
3. **Save Results**: Updates job with story ID and completion time
4. **Handle Errors**: If something goes wrong, marks job as "Failed"

#### `build_complete_story_tree()`
This function assembles a complete story from database pieces:
- Currently not implemented (marked as `pass`)
- Will eventually combine all story nodes into a tree structure

## Job Router

The job router (`job_router.py`) provides a simple way to check the status of story generation jobs.

### Endpoints

#### GET `/jobs/{job_id}`
**Purpose**: Check the status of a story generation job

**What happens**:
1. Looks up the job by its unique ID
2. Returns current status (pending, processing, completed, or failed)
3. If job doesn't exist, returns 404 error

**Parameters**:
- `job_id: str` - The unique identifier for the job
- `db: Session` - Database connection (auto-injected)

**Possible Responses**:
- `{"job_id": "abc123", "status": "pending"}` - Job is waiting to start
- `{"job_id": "abc123", "status": "processing"}` - Job is currently running
- `{"job_id": "abc123", "status": "completed", "story_id": 456}` - Job finished successfully
- `{"job_id": "abc123", "status": "failed", "error": "..."}` - Job encountered an error

## API Endpoints Summary

| Method | Endpoint | Purpose | Returns |
|--------|----------|---------|---------|
| POST | `/stories/create` | Start new story generation | Job details |
| GET | `/stories/{story_id}/complete` | Get complete story | Full story tree |
| GET | `/jobs/{job_id}` | Check job status | Job status info |

## FAQ

### Q: Why use background tasks instead of generating stories immediately?
**A**: Story generation might take several seconds or minutes. Background tasks let us:
- Return an immediate response to the user
- Show progress/status while processing
- Prevent request timeouts
- Handle multiple requests simultaneously

### Q: What happens if a user closes their browser?
**A**: The session ID is stored in a cookie, so when they return, they'll have the same session and can access their stories.

### Q: How are jobs and stories related?
**A**: 
- A **job** represents the process of creating a story
- A **story** is the actual content created by a completed job
- Jobs track progress; stories contain the final result

### Q: Why do we need separate routers for stories and jobs?
**A**: 
- **Stories router**: Handles story content and creation
- **Jobs router**: Handles process monitoring and status
- This separation makes the API clearer and more organized

### Q: What's the difference between `session_id` and `job_id`?
**A**: 
- **session_id**: Identifies a user's browser session (persists across multiple stories)
- **job_id**: Identifies a specific story generation task (unique per story)

### Q: How do I test these endpoints?
**A**: You can use:
- FastAPI's automatic documentation at `/docs`
- Tools like Postman or curl
- The frontend application that consumes these APIs
