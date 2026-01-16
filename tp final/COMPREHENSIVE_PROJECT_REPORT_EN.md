# Comprehensive Project Report: Electronic Medical Records System

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Middleware Implementation](#middleware-implementation)
4. [Role-Based Access Control (RBAC)](#role-based-access-control-rbac)
5. [Core Components](#core-components)
6. [Security Features](#security-features)
7. [User Experience Improvements](#user-experience-improvements)
8. [Technical Documentation](#technical-documentation)

---

## Project Overview

The Electronic Medical Records System is a comprehensive healthcare management application built with a 3-tier architecture using Python and FastAPI. The system implements robust security measures through custom middleware and role-based access control to ensure data privacy and appropriate access levels for different healthcare professionals.

### Key Features:
- Patient management (registration, viewing, updating, deletion)
- Medical reports generation and management
- Prescription handling
- Notification system
- Real-time statistics dashboard

---

## System Architecture

### Three-Tier Architecture (3-Tier)

#### 1. Presentation Layer
- **Location**: `templates/` directory
- **Components**: HTML templates (`home.html`, `login.html`)
- **Responsibilities**:
  - User interface rendering
  - Request handling and response presentation
  - Client-side validation and interactions

#### 2. Business Logic Layer
- **Location**: `main.py`
- **Components**: API endpoints, business validation, authentication logic
- **Responsibilities**:
  - Processing user requests
  - Implementing business rules
  - Coordinating between presentation and data layers

#### 3. Data Layer
- **Location**: `main.py` (database functions)
- **Database**: SQLite (`database.db`)
- **Components**: CRUD operations, data validation
- **Responsibilities**:
  - Data storage and retrieval
  - Database connection management
  - Transaction handling

---

## Middleware Implementation

### Purpose
Custom middleware was developed to centralize authentication and authorization processes, providing a secure and maintainable approach to access control.

### Key Components

#### 1. Authentication Middleware (`middleware/auth_middleware.py`)
```python
class AuthMiddleware:
    """Middleware for user authentication and permission checking"""
    
    async def __call__(self, scope, receive, send):
        # Intercept all HTTP requests
        # Extract user credentials from headers
        # Store user info in request scope
        # Continue processing or reject unauthorized requests
```

#### 2. Role Permissions Mapping
```python
ROLE_PERMISSIONS = {
    "Doctor": {
        "patients": ["read", "write", "update", "delete"],
        "reports": ["read", "write"],
        "prescriptions": ["read", "write"]
    },
    "Nurse": {
        "patients": ["read"],
        "reports": ["read"],
        "prescriptions": []
    },
    "Pharmacist": {
        "patients": ["read"],
        "reports": [],
        "prescriptions": ["read"]
    }
}
```

### Integration with FastAPI
```python
from middleware.auth_middleware import AuthMiddleware

app = FastAPI()
app.add_middleware(AuthMiddleware)
```

### Benefits
- Centralized security management
- Automatic permission checking for all API endpoints
- Reduced code duplication
- Enhanced maintainability

---

## Role-Based Access Control (RBAC)

### User Roles and Permissions

#### Doctor
- **Patients**: Full access (read, write, update, delete)
- **Reports**: Read and write
- **Prescriptions**: Read and write

#### Nurse
- **Patients**: Read-only access
- **Reports**: Read-only access
- **Prescriptions**: No access

#### Pharmacist
- **Patients**: Read-only access
- **Reports**: No access
- **Prescriptions**: Read-only access

### Implementation Details
```python
def check_permission(role: str, resource: str, action: str) -> bool:
    """Verify if user role has permission to perform action on resource"""
    if role not in ROLE_PERMISSIONS:
        return False
    if resource not in ROLE_PERMISSIONS[role]:
        return False
    return action in ROLE_PERMISSIONS[role][resource]
```

---

## Core Components

### 1. Main Application (`main.py`)
- FastAPI application setup
- API endpoints for all system functionalities
- Database integration
- Middleware integration

### 2. Database Initialization (`init_db.py`)
- Creates SQLite database tables
- Sets up initial user accounts
- Inserts sample patient data

### 3. HTML Templates (`templates/`)
- `home.html`: Main dashboard and user interface
- `login.html`: User authentication page

### 4. Custom Middleware (`middleware/auth_middleware.py`)
- Authentication and authorization logic
- Permission checking system

---

## Security Features

### 1. Header-Based Authentication
- User role passed via `X-User-Role` header
- Username passed via `X-User-Name` header
- Automatic validation on every request

### 2. Centralized Permission Checking
- All API endpoints protected by middleware
- Granular permissions per resource and action
- Immediate rejection of unauthorized requests

### 3. Role-Specific UI Elements
- Interface elements dynamically shown/hidden based on user role
- Action buttons (edit, delete) only visible to authorized users
- Navigation menu customized per role

### 4. Data Access Control
- Doctors: Full patient management
- Nurses: Read-only patient access
- Pharmacists: Patient viewing and prescription access

---

## User Experience Improvements

### 1. Welcome Message Enhancement
- Clear welcome message showing user role and name
- Consistent format across all user types
- English-only interface for uniformity

### 2. Navigation Improvements
- Pharmacists no longer auto-redirected to patients page
- Dashboard shown by default for all users
- Manual navigation to desired sections

### 3. Role-Based Interface Customization
- Appropriate cards and navigation links shown per role
- Action buttons hidden for unauthorized users
- Clean, uncluttered interface per user needs

### 4. Responsive Design
- Mobile-friendly layout
- Intuitive navigation
- Clear visual hierarchy

---

## Technical Documentation

### File Structure
```
project_root/
├── main.py                 # Main application
├── init_db.py              # Database initialization
├── middleware/
│   └── auth_middleware.py  # Custom middleware
├── templates/
│   ├── home.html           # Main dashboard
│   └── login.html          # Login page
├── database.db             # SQLite database
└── documentation/
    └── MIDDLEWARE_DOCUMENTATION_AR.md
```

### API Endpoints
- `GET /` - Login page
- `POST /login` - User authentication
- `GET /home` - Main dashboard
- `GET /api/patients` - Retrieve patients
- `POST /api/patients` - Create new patient
- `GET /api/patients/{id}` - Get specific patient
- `PUT /api/patients/{id}` - Update patient
- `DELETE /api/patients/{id}` - Delete patient
- `GET /api/reports` - Retrieve reports
- `POST /api/reports` - Create new report
- `GET /api/prescriptions` - Retrieve prescriptions
- `POST /api/prescriptions` - Create new prescription

### Running the Application
1. Execute `run_server.bat` or:
2. Activate virtual environment: `.venv\Scripts\activate`
3. Initialize database: `python init_db.py`
4. Start server: `uvicorn main:app --reload`

### Dependencies
- Python 3.x
- FastAPI
- Uvicorn
- SQLite (built-in)

---

## Conclusion

The Electronic Medical Records System successfully implements a robust 3-tier architecture with custom middleware for role-based access control. The system provides appropriate access levels for doctors, nurses, and pharmacists while maintaining a clean, user-friendly interface. Security is centralized through the middleware implementation, ensuring consistent protection across all system components.