# face-ai-service
# AI Face Platform

AI-powered employee face recognition and attendance management backend
built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Pydantic**,
and **InsightFace SCRFD**.

The platform provides an end-to-end workflow for employee management,
face registration, face recognition, face verification, attendance,
statistics, and dashboard APIs.

## Features

-   Employee management
-   Face detection with InsightFace SCRFD
-   Multi-image face registration
-   Face embedding generation and storage
-   One-to-many face recognition
-   One-to-one employee face verification
-   Recognition logging
-   Attendance check-in/check-out
-   Today's attendance
-   Attendance history
-   Employee attendance statistics
-   Monthly attendance statistics
-   Administrator dashboard
-   Employee-specific dashboard
-   Swagger/OpenAPI and ReDoc documentation

## System Workflow

``` text
Create Employee
      |
      v
Register Face Images
      |
      v
Generate Face Embeddings
      |
      v
Face Recognition / Verification
      |
      v
Attendance Check-In
      |
      v
Attendance Check-Out
      |
      v
Attendance History
      |
      v
Attendance Statistics
      |
      v
Dashboard
```

## Technology Stack

  Component              Technology
  ---------------------- ---------------------------
  API framework          FastAPI
  Language               Python 3.12
  ASGI server            Uvicorn
  Database               PostgreSQL
  ORM                    SQLAlchemy
  Validation             Pydantic
  Face detector          InsightFace SCRFD
  Numerical processing   NumPy
  API documentation      OpenAPI / Swagger / ReDoc
  Future client          Flutter

## Architecture

``` text
                    REST API
                       |
                       v
                 FastAPI Routes
                       |
        +--------------+--------------+
        |              |              |
        v              v              v
    Employees      Registration    Recognition
        |              |              |
        +--------------+--------------+
                       |
                       v
                    Services
                       |
        +--------------+--------------+
        |              |              |
        v              v              v
     Face AI       Attendance      Statistics
        |
        v
 InsightFace SCRFD
        |
        v
 Face Embeddings
        |
        v
 PostgreSQL
```

## Project Structure

``` text
face-ai-service/
|
+-- app/
|   +-- ai/
|   |   +-- detector/
|   |       +-- base_detector.py
|   |       +-- scrfd_detector.py
|   |
|   +-- api/
|   |   +-- routes.py
|   |   +-- health_routes.py
|   |   +-- employee_routes.py
|   |   +-- registration_routes.py
|   |   +-- recognition_routes.py
|   |   +-- attendance_routes.py
|   |   +-- attendance_statistics_routes.py
|   |   +-- dashboard_routes.py
|   |   +-- dependencies.py
|   |
|   +-- core/
|   |   +-- config.py
|   |   +-- logger.py
|   |   +-- model_loader.py
|   |
|   +-- db_models/
|   |   +-- employee.py
|   |   +-- face_profile.py
|   |   +-- attendance.py
|   |   +-- recognition_log.py
|   |
|   +-- database/
|   |
|   +-- schemas/
|   |   +-- employee.py
|   |   +-- registration.py
|   |   +-- recognition.py
|   |   +-- attendance.py
|   |   +-- dashboard.py
|   |
|   +-- services/
|       +-- registration_service.py
|       +-- recognition_service.py
|       +-- attendance_service.py
|       +-- attendance_statistics_service.py
|       +-- dashboard_service.py
|
+-- main.py
+-- requirements.txt
+-- .env
+-- README.md
```

## Requirements

Install:

-   Python 3.12
-   PostgreSQL
-   Git
-   Required InsightFace/SCRFD model environment

Create a virtual environment on Windows:

``` bash
python -m venv venv312
venv312\Scripts\activate
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

## Database Setup

Create a PostgreSQL database, for example:

``` sql
CREATE DATABASE attendance_ai;
```

Configure the database connection using the variables expected by
`app/core/config.py`.

A typical configuration is:

``` env
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/attendance_ai
```

Do not commit passwords or other secrets to Git.

## Environment Configuration

Create a `.env` file when required by the application.

Example:

``` env
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/attendance_ai
DEBUG=true
SCRFD_CTX_ID=0
```

The authoritative list of configuration variables is
`app/core/config.py`.

## AI Model

AI model initialization is handled by:

``` text
app/core/model_loader.py
```

The SCRFD detector wrapper is:

``` text
app/ai/detector/scrfd_detector.py
```

The detector provides face bounding boxes, landmarks, and detection
confidence.

## Running the API

From the `face-ai-service` directory:

``` bash
uvicorn app.main:app --reload
```

Or:

``` bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Default development URL:

``` text
http://127.0.0.1:8000
```

## API Documentation

Swagger UI:

``` text
http://127.0.0.1:8000/docs
```

ReDoc:

``` text
http://127.0.0.1:8000/redoc
```

OpenAPI JSON:

``` text
http://127.0.0.1:8000/openapi.json
```

## API Overview

All application endpoints use the `/api/v1` prefix.

### Health

``` text
GET /api/v1/health
```

### Employees

Employee endpoints are available under:

``` text
/api/v1/employees
```

### Face Registration

``` text
POST /api/v1/registration
GET  /api/v1/registration/{employee_id}
```

### Recognition

``` text
POST /api/v1/recognition/recognize
POST /api/v1/recognition/verify
POST /api/v1/recognition/verify/{employee_id}
```

### Attendance

``` text
POST   /api/v1/attendance/check-in
POST   /api/v1/attendance/check-out
GET    /api/v1/attendance/{employee_id}/today
GET    /api/v1/attendance/{employee_id}/history
GET    /api/v1/attendance/record/{attendance_id}
DELETE /api/v1/attendance/record/{attendance_id}
```

### Attendance Statistics

``` text
GET /api/v1/attendance/statistics/today
GET /api/v1/attendance/statistics/employee/{employee_id}
GET /api/v1/attendance/statistics/monthly
```

### Dashboard

``` text
GET /api/v1/dashboard/overview
GET /api/v1/dashboard/employee/{employee_id}
```

See `docs/API_DOCUMENTATION.md` for complete request and response
details.

## Attendance Workflow

### 1. Create Employee

Create the employee master record containing HR/business information.

### 2. Register Face

Register the employee's face using multiple images. The tested workflow
uses five images per employee.

The registration process performs:

1.  Face detection
2.  Detection validation
3.  Face embedding generation
4.  Profile storage
5.  Registration status tracking

### 3. Check Registration Status

``` text
GET /api/v1/registration/{employee_id}
```

### 4. Recognize Face

The recognition endpoint searches registered profiles and returns the
best match when the configured similarity threshold is satisfied.

### 5. Verify Employee

For one-to-one verification:

``` text
POST /api/v1/recognition/verify/{employee_id}
```

### 6. Check In

``` text
POST /api/v1/attendance/check-in
```

### 7. Check Out

``` text
POST /api/v1/attendance/check-out
```

### 8. View Attendance

``` text
GET /api/v1/attendance/{employee_id}/today
GET /api/v1/attendance/{employee_id}/history
```

### 9. Statistics

Use the attendance statistics endpoints for daily, employee, and monthly
reporting.

### 10. Dashboard

``` text
GET /api/v1/dashboard/overview
GET /api/v1/dashboard/employee/{employee_id}
```

## Example Recognition Response

``` json
{
  "recognized": true,
  "employee_id": 3,
  "employee_code": "EMP003",
  "employee_name": "Rajeev Sonkar",
  "similarity": 0.8418,
  "threshold": 0.62,
  "message": "Face recognized successfully."
}
```

## Example Verification Response

``` json
{
  "success": true,
  "employee_id": 3,
  "verified": true,
  "similarity": 0.8208,
  "confidence": 0.8208,
  "threshold": 0.62,
  "message": "Face verified successfully."
}
```

## Dashboard

The administrator dashboard aggregates:

-   Total employees
-   Active employees
-   Present today
-   Absent today
-   Late today
-   Checked in
-   Checked out
-   Attendance percentage
-   Department statistics
-   Attendance trend
-   Recent attendance
-   Recent recognition activity

The employee dashboard provides:

-   Employee information
-   Attendance statistics
-   Today's attendance
-   Recent attendance history

## Error Handling

Common HTTP responses:

  Status   Meaning
  -------- --------------------------------------------
  200      Successful request
  400      Invalid request or business-rule violation
  404      Resource not found
  422      Request validation failed
  500      Unexpected server-side failure

Always check the Uvicorn/FastAPI console for the underlying exception
during development.

## Testing

Recommended API testing sequence:

``` text
1. Health
2. Employee creation
3. Employee retrieval
4. Face registration
5. Registration status
6. Face recognition
7. Face verification
8. Check-in
9. Check-out
10. Today's attendance
11. Attendance history
12. Attendance statistics
13. Monthly statistics
14. Dashboard overview
15. Employee dashboard
```

The APIs can be tested using Swagger, ReDoc, Postman, curl, or a future
Flutter/mobile client.

## Security Notes

This application processes biometric information. Before production
deployment:

-   Enable HTTPS.
-   Add authentication and authorization.
-   Restrict CORS origins.
-   Protect biometric endpoints.
-   Secure stored biometric data.
-   Protect database credentials.
-   Do not commit `.env` or secrets.
-   Restrict administrative deletion operations.
-   Add appropriate audit logging.
-   Apply relevant privacy and biometric-data requirements.

The development configuration may be more permissive than a production
configuration.

## Current Status --- Face AI Service v1

``` text
Employee Management          [x]
Face Detection               [x]
Face Registration             [x]
Face Embedding                [x]
Face Recognition              [x]
Face Verification             [x]
Recognition Logging           [x]
Attendance Check-In           [x]
Attendance Check-Out          [x]
Attendance History            [x]
Attendance Statistics         [x]
Monthly Statistics            [x]
Dashboard Service             [x]
Dashboard API                 [x]
Swagger/API Testing           [x]
```

The core backend workflow has been implemented and verified
progressively through the API/Swagger testing workflow.

## Future Enhancements

Potential next steps:

-   Flutter/mobile application
-   Administrator authentication
-   Role-based access control
-   Live camera recognition
-   Real-time dashboard updates
-   WebSocket recognition activity
-   Advanced attendance analytics
-   CSV/Excel/PDF exports
-   Holiday and leave management
-   Shift management
-   Multiple office/location support
-   Liveness detection
-   Anti-spoofing improvements
-   Biometric encryption
-   Docker deployment
-   Automated unit and integration tests
-   CI/CD pipeline
-   Production deployment

## License

Add the project's chosen license before public distribution.

## Author

**Sanghmitra Maheshwari**

AI Face Platform\
Face Recognition & Employee Attendance Backend
