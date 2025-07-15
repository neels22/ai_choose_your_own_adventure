# Models Documentation 📊

This folder contains all the database models for our AI Choose Your Own Adventure application. Understanding these models is crucial as they define the data structure and relationships that power our entire system.

## Table of Contents
- [Overview](#overview)
- [Why Models Matter](#why-models-matter)
- [SQLAlchemy & ORM Explained](#sqlalchemy--orm-explained)
- [Understanding Imports](#understanding-imports)
- [Story Model](#story-model)
- [StoryNode Model](#storynode-model)
- [StoryJob Model](#storyjob-model)
- [Relationships Explained](#relationships-explained)
- [Data Structure Visualization](#data-structure-visualization)
- [Async Job Processing Flow](#async-job-processing-flow)

## Overview

Our application uses three main models to represent data:

1. **Story** - Represents the main story container
2. **StoryNode** - Represents individual story segments in a tree structure
3. **StoryJob** - Handles asynchronous story generation tasks

These models work together to create an interactive storytelling experience where users can navigate through branching narratives.

## Why Models Matter

Understanding the data structure is fundamental because:
- **Data Relationships**: Shows how different pieces of information connect
- **System Architecture**: Helps understand how the application works internally
- **Database Design**: Defines how data is stored and retrieved
- **API Design**: Models directly influence our API endpoints and responses

## SQLAlchemy & ORM Explained

### What is SQLAlchemy?
SQLAlchemy is a Python Object-Relational Mapping (ORM) library that allows us to:
- Work with databases using Python classes instead of raw SQL
- Map database tables to Python objects automatically
- Handle database relationships in an object-oriented way
- Provide database abstraction (works with different database types)

### What is ORM?
Object-Relational Mapping bridges the gap between:
- **Object-Oriented Programming** (Python classes)
- **Relational Databases** (tables, rows, columns)

Instead of writing SQL queries like:
```sql
SELECT * FROM stories WHERE session_id = 'abc123';
```

We can use Python code like:
```python
stories = session.query(Story).filter(Story.session_id == 'abc123').all()
```

## Understanding Imports

Let's break down each import and its purpose:

```python
from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime, Boolean
```

### Import Breakdown:

| Import | Purpose | Example Usage |
|--------|---------|---------------|
| `Column` | Defines a database column in our table | `id = Column(Integer, primary_key=True)` |
| `Integer` | Data type for whole numbers | User IDs, counts, references |
| `String` | Data type for text | Titles, content, names |
| `JSON` | Data type for structured data | Lists, dictionaries, complex objects |
| `ForeignKey` | Creates relationships between tables | Links StoryNode to Story |
| `DateTime` | Data type for dates and times | Creation timestamps, completion times |
| `Boolean` | Data type for True/False values | Flags like is_root, is_ending |

```python
from sqlalchemy.sql import func
```
- **Purpose**: Provides SQL functions like `now()` for timestamps
- **Usage**: `server_default=func.now()` automatically sets creation time

```python
from sqlalchemy.orm import relationship
```
- **Purpose**: Defines relationships between models
- **Usage**: Links Story to StoryNodes, enables navigation between related objects

```python
from db.database import Base
```
- **Purpose**: Imports the declarative base class
- **Why needed**: All our models must inherit from `Base` to be recognized by SQLAlchemy
- **What it does**: Provides the foundation for creating database tables

## Story Model

The `Story` class represents the main container for each interactive story.

```python
class Story(Base):
    __tablename__ = "stories"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    session_id = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    nodes = relationship("StoryNode", back_populates="story")
```

### Field Explanations:

| Field | Type | Purpose | Details |
|-------|------|---------|---------|
| `id` | Integer | Unique identifier | Primary key, auto-incremented, indexed for fast lookups |
| `title` | String | Story name/title | Indexed for search performance |
| `session_id` | String | User session tracking | Links story to specific user session, indexed |
| `created_at` | DateTime | Creation timestamp | Automatically set when story is created, timezone-aware |
| `nodes` | Relationship | Connected story nodes | One-to-many relationship with StoryNode |

### Key Concepts:

- **Primary Key**: `id` uniquely identifies each story
- **Index**: Creates database indexes for faster queries on frequently searched fields
- **Server Default**: `func.now()` automatically sets timestamp on the database side
- **Timezone Awareness**: Handles time zones correctly for global applications

## StoryNode Model

The `StoryNode` class represents individual segments of the story in a tree structure.

```python
class StoryNode(Base):
    __tablename__ = "story_nodes"
    
    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id"), index=True)
    content = Column(String, index=True)
    is_root = Column(Boolean, default=False)
    is_ending = Column(Boolean, default=False)
    is_winning_ending = Column(Boolean, default=False)
    options = Column(JSON, default=list)
    
    story = relationship("Story", back_populates="nodes")
```

### Field Explanations:

| Field | Type | Purpose | Details |
|-------|------|---------|---------|
| `id` | Integer | Unique node identifier | Primary key for each story segment |
| `story_id` | Integer | Links to parent story | Foreign key reference to stories.id |
| `content` | String | Story text content | The actual narrative text for this node |
| `is_root` | Boolean | Marks starting node | True for the first node of the story |
| `is_ending` | Boolean | Marks terminal nodes | True for nodes that end the story |
| `is_winning_ending` | Boolean | Marks successful endings | True for positive story conclusions |
| `options` | JSON | Available choices | List of options for user to choose next path |
| `story` | Relationship | Parent story reference | Links back to the containing Story |

### Story Tree Structure:

Each story forms a tree where:
- **Root Node**: Starting point (is_root=True)
- **Branch Nodes**: Middle segments with multiple options
- **Leaf Nodes**: Ending points (is_ending=True)

Example tree structure:
```
     Story Start (Root)
    /              \    
   Go Left        Go Right
  /      \        /      \
Death   Success  Trap   Victory
(End)   (Win)    (End)   (Win)
```

## StoryJob Model

The `StoryJob` class manages asynchronous story generation tasks.

```python
class StoryJob(Base):
    __tablename__ = "story_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, index=True, unique=True)
    session_id = Column(String, index=True)
    theme = Column(String)
    status = Column(String)
    story_id = Column(Integer, nullable=True)
    error = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
```

### Field Explanations:

| Field | Type | Purpose | Details |
|-------|------|---------|---------|
| `id` | Integer | Unique job identifier | Primary key for each generation job |
| `job_id` | String | External job reference | Unique identifier for frontend tracking |
| `session_id` | String | User session tracking | Links job to specific user session |
| `theme` | String | Story theme/genre | User-selected story theme (e.g., "fantasy", "sci-fi") |
| `status` | String | Job progress state | "pending", "in_progress", "completed", "failed" |
| `story_id` | Integer | Generated story reference | Links to created Story (null until completion) |
| `error` | String | Error information | Error message if job fails (null on success) |
| `created_at` | DateTime | Job creation time | When job was initiated |
| `completed_at` | DateTime | Job completion time | When job finished (null while running) |

### Why We Need StoryJob:

Story generation using AI can take significant time (10-60 seconds). Without async jobs:
- ❌ Frontend would freeze waiting for response
- ❌ HTTP requests would timeout
- ❌ Poor user experience
- ❌ Server resources locked during generation

With async jobs:
- ✅ Immediate response with job ID
- ✅ Frontend can poll for status
- ✅ Better user experience with progress indicators
- ✅ Server can handle multiple requests simultaneously

## Relationships Explained

### One-to-Many Relationship (Story ↔ StoryNode)

```python
# In Story model
nodes = relationship("StoryNode", back_populates="story")

# In StoryNode model  
story = relationship("Story", back_populates="nodes")
```

### What this means:
- **One Story** can have **many StoryNodes**
- **Each StoryNode** belongs to **exactly one Story**
- **back_populates**: Creates bidirectional relationship

### How it works:
```python
# Get all nodes for a story
story = session.query(Story).first()
all_nodes = story.nodes  # Returns list of StoryNode objects

# Get parent story from a node
node = session.query(StoryNode).first()
parent_story = node.story  # Returns Story object
```

### Benefits:
- **Navigation**: Easy to move between related objects
- **Data Integrity**: Foreign key constraints prevent orphaned data
- **Query Optimization**: SQLAlchemy can optimize joins automatically

## Data Structure Visualization

### Story Tree Representation:
```
Story: "Haunted Castle Adventure"
├── Root Node: "You approach a dark castle..."
│   ├── Option 1: "Enter through main door"
│   │   ├── Node: "The door creaks open..."
│   │   │   ├── Option: "Go upstairs" → Success Ending
│   │   │   └── Option: "Go to basement" → Death Ending
│   │   └── ...
│   └── Option 2: "Sneak around back"
│       ├── Node: "You find a garden..."
│       │   ├── Option: "Climb the wall" → Victory Ending
│       │   └── Option: "Hide in bushes" → Death Ending
│       └── ...
```

### Database Relationship Diagram:
```
┌─────────────────┐         ┌─────────────────┐
│     Story       │────────▶│   StoryNode     │
├─────────────────┤ 1   ∞   ├─────────────────┤
│ id (PK)         │         │ id (PK)         │
│ title           │         │ story_id (FK)   │
│ session_id      │         │ content         │
│ created_at      │         │ is_root         │
└─────────────────┘         │ is_ending       │
                            │ is_winning_ending│
                            │ options (JSON)  │
                            └─────────────────┘

┌─────────────────┐
│   StoryJob      │
├─────────────────┤
│ id (PK)         │
│ job_id (UNIQUE) │
│ session_id      │
│ theme           │
│ status          │
│ story_id        │
│ error           │
│ created_at      │
│ completed_at    │
└─────────────────┘
```

## Async Job Processing Flow

### Step-by-Step Process:

1. **Job Creation**:
   ```
   Frontend Request: "Create fantasy story"
   ↓
   Backend: Creates StoryJob with status="pending"
   ↓
   Response: Returns job_id to frontend
   ```

2. **Background Processing**:
   ```
   Backend: Updates job status="in_progress"
   ↓
   AI Generation: Creates story content
   ↓
   Database: Creates Story and StoryNode records
   ↓
   Backend: Updates job status="completed", story_id=new_story_id
   ```

3. **Status Polling**:
   ```
   Frontend: Polls "GET /jobs/{job_id}/status"
   ↓
   Backend: Returns current job status
   ↓
   If completed: Frontend gets story_id and fetches story
   ```

### Job Status Flow:
```
pending → in_progress → completed
                    ↓
                   failed (if error occurs)
```

### Benefits of This Pattern:
- **Responsiveness**: Frontend stays interactive
- **Scalability**: Multiple jobs can run concurrently  
- **Reliability**: Failed jobs can be retried
- **Monitoring**: Easy to track job progress and debug issues
- **User Experience**: Can show progress indicators and estimated completion times

---

This documentation provides a complete understanding of our data models and their relationships. Each model serves a specific purpose in creating an engaging, scalable interactive storytelling experience.
    