# Schemas Documentation

## Table of Contents
- [Overview](#overview)
- [What is Pydantic?](#what-is-pydantic)
- [Naming Conventions](#naming-conventions)
- [Story Schemas](#story-schemas)
- [Job Schemas](#job-schemas)
- [Usage Examples](#usage-examples)

## Overview

The `schemas` folder contains **data validation and serialization models** for our AI Choose Your Own Adventure application. These schemas define the structure and types of data that our API endpoints accept (requests) and return (responses).

### Purpose of Schemas
- **Data Validation**: Automatically validate incoming data to ensure it meets our requirements
- **Type Safety**: Define clear data types for better code reliability and IDE support
- **API Documentation**: FastAPI automatically generates API documentation from these schemas
- **Serialization**: Convert between Python objects and JSON for API communication
- **Code Organization**: Centralize all data structure definitions in one place

### Files in This Folder
- `story_schema.py`: Schemas related to story creation, nodes, and responses
- `job_schema.py`: Schemas for background job processing (story generation is async)

## What is Pydantic?

[Pydantic](https://docs.pydantic.dev/) is a Python library that provides **data validation using Python type annotations**. Here's why we use it:

### Core Components

#### BaseModel
```python
from pydantic import BaseModel
```
- **Purpose**: Base class that all our schemas inherit from
- **Features**: Provides automatic validation, serialization, and type conversion
- **Why We Use It**: Ensures data integrity and provides clear structure definitions

#### Field
```python
from pydantic import Field
```
- **Purpose**: Add additional validation rules and metadata to fields
- **Examples**: Default values, validation constraints, descriptions
- **Usage**: `Field(default=None, description="Optional field")`

#### Type Annotations
```python
from typing import List, Optional, Dict
```
- **List[Type]**: Represents a list containing elements of a specific type
- **Optional[Type]**: Means the field can be `None` or the specified type
- **Dict[KeyType, ValueType]**: Represents a dictionary with specific key/value types

## Naming Conventions

Our schemas follow specific naming patterns that indicate their purpose:

### Convention Meanings

| Suffix/Pattern | Purpose | Example | Usage |
|----------------|---------|---------|-------|
| `Base` | Parent class with common fields | `StoryBase` | Inherited by other schemas |
| `Request` | Data coming INTO our API | `CreateStoryRequest` | Request payloads |
| `Response` | Data going OUT of our API | `CompleteStoryResponse` | API responses |
| `Create` | Specifically for creation operations | `StoryJobCreate` | Creating new resources |
| `Schema` | General data structure | `StoryOptionsSchema` | Reusable components |

### Why Use "Base" Classes?
- **Code Reuse**: Common fields defined once and inherited by related schemas
- **Consistency**: Ensures related schemas have the same structure for shared fields
- **Maintainability**: Changes to common fields only need to be made in one place

## Story Schemas

### StoryOptionsSchema
```python
class StoryOptionsSchema(BaseModel):
    text: str
    node_id: Optional[int] = None
```

**Purpose**: Represents a choice/option that users can make in the story

**Fields Explained**:
- `text`: The text displayed for this choice (e.g., "Go left", "Fight the dragon")
- `node_id`: The ID of the story node this choice leads to (None for ending choices)

**Used In**: Story nodes to define available user choices

### StoryNodeBase
```python
class StoryNodeBase(BaseModel):
    content: str
    is_ending: bool = False
    is_winning_ending: bool = False
```

**Purpose**: Base class for story nodes (individual story segments)

**Fields Explained**:
- `content`: The actual story text for this node
- `is_ending`: Whether this node ends the story (default: False)
- `is_winning_ending`: Whether this is a successful ending (default: False)

**Why "Base"**: Other node-related schemas inherit these common fields

### CompleteStoryNodeResponse
```python
class CompleteStoryNodeResponse(StoryNodeBase):
    id: int
    options: List[StoryOptionsSchema] = []
    
    class Config:
        from_attributes = True
```

**Purpose**: Complete story node data sent to frontend/API clients

**Why Inherits StoryNodeBase**: Gets content, is_ending, and is_winning_ending fields automatically

**Additional Fields**:
- `id`: Unique identifier for this node in the database
- `options`: List of choices available from this node

**Why "Response"**: This schema formats data being sent OUT of our API

#### class Config and from_attributes

```python
class Config:
    from_attributes = True
```

**What is Config?**: Pydantic configuration class that customizes how the schema behaves

**What is from_attributes?**: 
- Allows Pydantic to create this schema from object attributes (like database models)
- **Example**: If you have a database object with `.id`, `.content`, `.options` attributes, Pydantic can automatically create a `CompleteStoryNodeResponse` from it
- **Why Important**: Enables seamless conversion from database objects to API responses

### StoryBase
```python
class StoryBase(BaseModel):
    title: str
    session_id: Optional[str] = None
    
    class Config:
        from_attributes = True
```

**Purpose**: Base class for story-related schemas with common story fields

**Fields Explained**:
- `title`: Name/title of the story
- `session_id`: Optional session identifier to track user sessions

### CreateStoryRequest
```python
class CreateStoryRequest(BaseModel):
    theme: str
```

**Purpose**: Data structure for creating new stories

**Why Separate from StoryBase**: Creation only needs theme; other fields (title, session_id) are generated or optional

**Usage**: When users request a new story via API

### CompleteStoryResponse
```python
class CompleteStoryResponse(StoryBase):
    id: int
    created_at: datetime
    root_node: CompleteStoryNodeResponse
    all_nodes: Dict[int, CompleteStoryNodeResponse]
    
    class Config:
        from_attributes = True
```

**Purpose**: Complete story data with all nodes, sent to clients

**Why Inherits StoryBase**: Gets title and session_id automatically

**Additional Fields**:
- `id`: Unique story identifier
- `created_at`: When the story was created
- `root_node`: The starting node of the story
- `all_nodes`: Dictionary mapping node IDs to their complete data

**Complex Types Explained**:
- `Dict[int, CompleteStoryNodeResponse]`: A dictionary where keys are integers (node IDs) and values are complete node objects

## Job Schemas

Background job processing is used because story generation takes time. Instead of making users wait, we:
1. Accept the request immediately
2. Return a job ID
3. Process the story generation in the background
4. Allow users to check job status

### StoryJobBase
```python
class StoryJobBase(BaseModel):
    theme: str
```

**Purpose**: Base class for job-related schemas

**Fields**: 
- `theme`: The story theme requested by the user

### StoryJobResponse
```python
class StoryJobResponse(BaseModel):
    job_id: str
    status: str
    created_at: datetime
    story_id: Optional[int] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    
    class Config:
        from_attributes = True
```

**Purpose**: Job status information sent to clients

**Fields Explained**:
- `job_id`: Unique identifier for tracking this job
- `status`: Current job state ("pending", "processing", "completed", "failed")
- `created_at`: When the job was created
- `story_id`: ID of the generated story (only set when completed successfully)
- `completed_at`: When the job finished (success or failure)
- `error`: Error message if the job failed

**Optional Fields**: Fields that might be None depending on job status

### StoryJobCreate
```python
class StoryJobCreate(StoryJobBase):
    pass
```

**Purpose**: Schema for creating new story generation jobs

**Why Inherits StoryJobBase**: Gets the `theme` field automatically

**Why "pass"**: No additional fields needed beyond what's in the base class

**Usage**: When clients request new story generation

## Usage Examples

### API Request Flow
1. **Create Story Request**:
   ```json
   POST /stories/
   {
     "theme": "medieval fantasy"
   }
   ```
   Uses: `CreateStoryRequest`

2. **Job Created Response**:
   ```json
   {
     "job_id": "abc123",
     "status": "pending",
     "created_at": "2024-01-01T10:00:00Z"
   }
   ```
   Uses: `StoryJobResponse`

3. **Check Job Status**:
   ```json
   GET /jobs/abc123
   {
     "job_id": "abc123",
     "status": "completed",
     "story_id": 42,
     "completed_at": "2024-01-01T10:02:00Z"
   }
   ```
   Uses: `StoryJobResponse`

4. **Get Complete Story**:
   ```json
   GET /stories/42
   {
     "id": 42,
     "title": "The Dragon's Quest",
     "root_node": {
       "id": 1,
       "content": "You stand before a dark castle...",
       "options": [
         {"text": "Enter the castle", "node_id": 2},
         {"text": "Walk away", "node_id": 3}
       ]
     },
     "all_nodes": { ... }
   }
   ```
   Uses: `CompleteStoryResponse`

### Benefits of This Schema Design
- **Type Safety**: Catch errors at development time
- **Auto-validation**: Invalid data is rejected automatically
- **Self-documenting**: Schemas serve as API documentation
- **Consistency**: All related data follows the same patterns
- **Extensibility**: Easy to add new fields or create new schemas
