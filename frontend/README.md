# 🎨 Frontend Workflow Documentation

## 🧭 Overview

The frontend is an **Interactive Story Generator** built with **Next.js 14** and **React 18** with TypeScript. This web application allows users to:

- **User-facing goal**: Create and play personalized choose-your-own-adventure stories
- **Story types**: Interactive, branching narratives based on user-provided themes (e.g., pirates, space, medieval)
- **User interaction**: Theme input → Story generation → Interactive decision-making gameplay
- **Framework**: Next.js with React, TypeScript, Tailwind CSS, and Axios for API communication

The application creates immersive storytelling experiences where users navigate through branching storylines by making choices that determine their adventure's outcome.

---

## 🧩 Component Structure

### Pages

#### **Root Page (`/`)**
- **File**: `src/app/page.tsx`
- **Purpose**: Landing page and entry point for new stories
- **Content**: Header + `StoryGenerator` component
- **User Flow**: First page users see when visiting the application

#### **Story Page (`/story/[id]`)**
- **File**: `src/app/story/[id]/page.tsx`
- **Purpose**: Displays and allows interaction with generated stories
- **Content**: Header + `StoryLoader` component
- **User Flow**: Where users experience the interactive storytelling

#### **Layout (`layout.tsx`)**
- **File**: `src/app/layout.tsx`
- **Purpose**: Global layout wrapper with metadata and fonts
- **Features**: Inter font, SEO metadata, and consistent styling

### Core Components

#### **StoryGenerator** (`src/components/StoryGenerator.tsx`)
- **Purpose**: Orchestrates the entire story creation process
- **State Management**:
  - `theme`: User's input theme
  - `jobId`: Background job identifier for story generation
  - `jobStatus`: Current status of story generation job
  - `loading`: Loading state indicator
  - `error`: Error message handling
- **Key Features**:
  - Handles theme submission
  - Manages asynchronous job polling
  - Navigates to story page upon completion
  - Error handling and retry functionality

#### **ThemeInput** (`src/components/ThemeInput.tsx`)
- **Purpose**: Form interface for capturing user's story theme
- **Props**: `onSubmit(theme: string) => void`
- **Features**:
  - Text input with validation
  - Placeholder examples (pirates, space, medieval)
  - Error display for empty submissions
- **User Flow**: First interaction point for users

#### **StoryLoader** (`src/components/StoryLoader.tsx`)
- **Purpose**: Fetches and prepares story data for gameplay
- **Props**: `id: number` (story ID from URL params)
- **State Management**:
  - `story`: Complete story data including all nodes
  - `loading`: Fetch status
  - `error`: Error handling for missing/failed stories
- **Features**:
  - Loads complete story structure from API
  - Error handling for 404s
  - Navigation back to story generator

#### **StoryGame** (`src/components/StoryGame.tsx`)
- **Purpose**: Core interactive gameplay component
- **Props**: 
  - `story`: Complete story object
  - `onNewStory(): void`: Callback for creating new stories
- **State Management**:
  - `currentNodeId`: Tracks user's current position in story
  - `currentNode`: Current story node data
  - `options`: Available choices for current node
  - `isEnding`: Whether current node is an ending
  - `isWinningEnding`: Whether it's a winning vs. losing ending
- **Features**:
  - Node navigation through story tree
  - Option selection handling
  - Ending detection and display
  - Restart functionality

#### **LoadingStatus** (`src/components/LoadingStatus.tsx`)
- **Purpose**: User-friendly loading interface
- **Props**: `theme: string`
- **Features**:
  - Animated spinner
  - Dynamic messaging based on theme
  - Provides feedback during story generation

---

## 🔁 User Interaction Flow

### 1. **Landing Page**
```
User visits "/" → Sees "Interactive Story Generator" header
                → ThemeInput form displayed
                → Placeholder: "Enter a theme (e.g. pirates, space, medieval...)"
```

### 2. **Story Generation Trigger**
```
User enters theme → Clicks "Generate Story" → Validation check
                                          → API POST /stories/create
                                          → Response: {job_id, status}
                                          → Loading screen appears
```

**API Request Example**:
```json
POST http://localhost:8000/api/stories/create
{
  "theme": "space adventure"
}
```

**Response**:
```json
{
  "job_id": "job_123",
  "status": "processing"
}
```

### 3. **Background Job Polling**
```
Every 5 seconds → GET /jobs/{job_id} → Check status
                                     → "processing" → Continue polling
                                     → "completed" → Navigate to story
                                     → "failed" → Show error
```

### 4. **Displaying the Story**
```
Navigation to /story/{story_id} → StoryLoader fetches complete story
                                → GET /stories/{id}/complete
                                → Story structure loaded
                                → StoryGame component renders root node
```

**Story Structure**:
```json
{
  "id": 1,
  "title": "Space Adventure",
  "theme": "space",
  "root_node": { "id": 1, "content": "...", "options": [...] },
  "all_nodes": {
    "1": { "id": 1, "content": "You wake up on a spaceship...", "options": [...] },
    "2": { "id": 2, "content": "You enter the engine room...", "is_ending": false },
    ...
  }
}
```

### 5. **Story Traversal**
```
Current node displayed → Options shown as buttons
                      → User clicks option → setCurrentNodeId(option.node_id)
                      → New node content loads → New options appear
                      → Continue until reaching ending node
```

### 6. **Ending the Story**
```
Node with is_ending: true → Hide options
                          → Show ending message
                          → Display win/lose status based on is_winning_ending
                          → Show "Restart Story" and "New Story" buttons
```

---

## 🧠 State Management

### **Strategy**: React Hooks (useState, useEffect)

### **Key State Variables**:

#### **StoryGenerator Component**:
- `theme: string` - User's input theme
- `jobId: string | null` - Background job identifier
- `jobStatus: string | null` - Job progress status
- `loading: boolean` - UI loading state
- `error: string | null` - Error messages

#### **StoryGame Component**:
- `currentNodeId: number | null` - User's position in story tree
- `currentNode: any` - Complete current node data
- `options: any[]` - Available choices
- `isEnding: boolean` - End-of-story detection
- `isWinningEnding: boolean` - Win/lose determination

### **State Flow**:
```
ThemeInput → StoryGenerator (theme) → API job creation → Polling loop
                                   → Story completion → Navigation
StoryLoader → StoryGame (story data) → Node navigation → Ending
```

---

## 🌐 API Integration

### **Base Configuration**:
```javascript
// src/utils/util.js
export const API_BASE_URL = "http://localhost:8000/api";
```

### **API Endpoints**:

#### **Story Creation**:
```javascript
POST /stories/create
Body: { theme: string }
Response: { job_id: string, status: string }
```

#### **Job Status Polling**:
```javascript
GET /jobs/{job_id}
Response: { 
  status: "processing" | "completed" | "failed",
  story_id?: number,
  error?: string 
}
```

#### **Story Retrieval**:
```javascript
GET /stories/{id}/complete
Response: {
  id: number,
  title: string,
  theme: string,
  root_node: Node,
  all_nodes: { [id: string]: Node }
}
```

### **Error Handling**:
- **Network errors**: Caught and displayed with retry options
- **404 errors**: "Story not found" message with navigation to generator
- **Job failures**: Error messages with reset functionality
- **Validation errors**: Form-level feedback for empty themes

---

## 🎨 UI/UX Details

### **Styling Approach**:
- **CSS Custom Properties** for consistent theming
- **Responsive design** with max-width containers
- **Color scheme**: Blue/teal theme with success/error states

### **Key Design Elements**:

#### **Color Palette**:
```css
--primary-color: #4a6fa5;
--secondary-color: #166d89;
--accent-color: #48cae4;
--success-color: #4caf50;
--error-color: #f44336;
```

#### **Loading Animation**:
- Spinner animation during story generation
- Dynamic messaging: "Generating Your {theme} Story"
- User feedback: "Please wait while we generate your story..."

#### **Interactive Elements**:
- **Option buttons**: Styled with hover effects for story choices
- **Error states**: Clear error messages with retry functionality
- **Navigation controls**: "Restart Story" and "New Story" buttons

#### **Layout Structure**:
```
.app-container (max-width: 800px, centered)
  header
    h1: Interactive Story Generator
  main
    Component content (StoryGenerator | StoryLoader)
```

### **Responsive Features**:
- Centered layout with max-width for readability
- Mobile-friendly button sizes and spacing
- Consistent padding and margins across screen sizes

---

## 🧪 Testing & Debugging

### **Development Setup**:
```bash
npm run dev    # Development server on localhost:3000
npm run build  # Production build
npm run lint   # Code linting
```

### **Common Debug Points**:
- **Job polling**: Check browser network tab for 5-second intervals
- **Navigation**: Verify router.push() calls in browser console
- **API responses**: Monitor API calls and response format
- **State updates**: Use React DevTools to track state changes

### **Error Scenarios to Test**:
- Empty theme submission
- Network connectivity issues
- Invalid story IDs
- Job timeout/failure scenarios

---

## 📝 Summary

### **Complete User Journey**:

1. **Landing** → User visits homepage with theme input form
2. **Theme Entry** → User enters desired story theme (e.g., "pirates")
3. **Generation** → Async job created, loading screen with polling
4. **Navigation** → Automatic redirect to `/story/{id}` when complete
5. **Gameplay** → Interactive decision-making through story nodes
6. **Ending** → Win/lose scenarios with restart/new story options

### **Technical Flow**:
```
Next.js App → React Components → Axios API Calls → FastAPI Backend
    ↓              ↓                    ↓              ↓
  Routing    State Management    HTTP Requests    Story Generation
```

### **Key Features**:
- **Asynchronous Processing**: Background job system for story generation
- **Real-time Updates**: Polling mechanism for job status
- **Interactive Navigation**: Seamless story traversal
- **Error Resilience**: Comprehensive error handling and recovery
- **Responsive Design**: Mobile-friendly interface

The frontend creates a smooth, engaging storytelling experience by orchestrating theme input, asynchronous story generation, and interactive gameplay into a cohesive user journey. The component architecture ensures maintainable code while providing rich user interactions for the choose-your-own-adventure experience. 