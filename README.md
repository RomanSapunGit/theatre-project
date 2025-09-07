# 🎭 Theatre Project

A Django-based web application for managing theatre plays, performances, reservations, and tickets.  
Includes REST API endpoints built with Django REST Framework (DRF), authentication with JWT, and automated testing.

---

## Table of Contents

- [Overview](#overview)  
- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Testing](#testing)  
- [Project Structure](#project-structure)  
- [Contributing](#contributing)  

---

## Overview

The **Theatre Project** allows theatre administrators and staff to manage plays, performances, and reservations.  
Users can register, book tickets, and receive verification codes via email.  
The project is designed to demonstrate best practices in Django, DRF, testing, and API design.

---

## Features

- Manage plays, genres, and images  
- Schedule performances in different theatre halls  
- Make reservations and issue tickets  
- User authentication with JWT  
- Email verification system  
- API endpoints with DRF ViewSets and Routers  
- Automated tests for models, views, and queries  

---

## Tech Stack

- **Backend:** Django, Django REST Framework  
- **Database:** PostgreSQL (or SQLite for dev)  
- **Auth:** JWT, Django Authentication System  
- **Tools:** Docker (optional), Postman / Swagger for API docs  
- **Testing:** Django TestCase, DRF test client  

---

## Installation

1. **Clone the repository**  
   ```
   git clone https://github.com/RomanSapunGit/theatre-project.git
   cd theatre-project
   ```
2. **Create and activate virtual environment**
    ```
   python -m venv venv
    source venv/bin/activate   # Linux/Mac
    venv\Scripts\activate     # Windows
   ```
3. **Install dependencies**
    ```
   pip install -r requirements.txt
   ```
4. **Apply migrations**
    ```python manage.py migrate```
5. **Add .env file**
   #### environment variables needed to add:
    ```
    PYTHONUNBUFFERED	
       - Ensures Python output is sent straight to the terminal (recommended value: 1).
    POSTGRES_DB	
       - Name of the PostgreSQL database used by Django.
    POSTGRES_USER	
       - PostgreSQL username.
    POSTGRES_PASSWORD	
       - Password for the PostgreSQL user.
    POSTGRES_HOST	
       - Hostname of the PostgreSQL server (e.g., db for Docker service).
    POSTGRES_DB_PORT	
       - Port for PostgreSQL (default 5432).
    SECRET_KEY	
       - Django secret key used for cryptographic signing. Keep it secure.
    EMAIL_HOST_USER	
       - Email address used for sending verification and notification emails.
    EMAIL_HOST_PASSWORD	
       - Password or app-specific token for the email account.
    ```
6. **Load fixtures (sample data)**
    ```python manage.py loaddata theatre_data.json```
7. **Start development server**
    ```python manage.py runserver```

### or simply using docker:

1. **Build and start Docker containers**  
``` docker-compose up --build```
2. **Access the development server**
```http://0.0.0.0:8000/```

## Usage
- API root:
```http://127.0.0.1:8000/api/```
- Example endpoints:
- **List Plays:** `GET /api/plays/`  
- **Play Detail:** `GET /api/plays/<id>/`  
- **Upload Play Image:** `POST /api/plays/<id>/upload-image/`  
- **List Reservations:** `GET /api/reservations/`  
- **Create Performance:** `POST /api/performances/` 
- Authentication:
- Obtain JWT token: `POST /api/token/`  
- Refresh token: `POST /api/token/refresh/`  

---

## Testing

Run the test suite:

```python manage.py test```
or
```coverage run manage.py test``` to see the test coverage and test results.
To see test coverage, use ```coverage html```

Tests cover:

- API responses and behavior

- Query efficiency (prevents duplicate queries)

- Permissions and authentication

- Business logic validation

---
## Project Structure
```theatre-project/
├── theatre_project/                # Django project settings
│   ├── __init__.py
│   ├── asgi.py                     # ASGI entrypoint for async support
│   ├── settings.py                 # Main project settings
│   ├── urls.py                     # Root URL configurations
│   └── wsgi.py                     # WSGI entrypoint for deployment
│
├── theatre/                        # Main Django app
│   ├── __init__.py
│   ├── management/                  
│   │     ├── __init__.py
│   │     └── ... (wait_for_db.py)   # Custom command for reconnecting to db (used in docker container)
│   ├── admin.py                     # Django admin customizations
│   ├── apps.py                      # App configuration
│   ├── models.py                    # Database models: Play, Performance, Ticket, Reservation, etc.
│   ├── serializers.py               # DRF serializers for API endpoints
│   ├── views.py                     # API views (ViewSets, APIViews)
│   ├── urls.py                      # App-level URL routes
│   ├── permissions.py               # Custom permissions for DRF
│   ├── tests.py                     # Automated tests for theatre app
│   ├── utils.py                     # Helper functions (e.g., create_user_reservation)
│   └── migrations/                  # Auto-generated migration files
│       ├── __init__.py              
│       └── ... (migration files)
│
├── user/                           # Custom user management app
│   ├── __init__.py
│   ├── admin.py                     # Admin for user model
│   ├── apps.py                      # App configuration
│   ├── models.py                    # Custom User model
│   ├── serializers.py               # User-related serializers
│   ├── tests.py                     # Automated tests for theatre app
│   ├── views.py                     # User-related API views
│   ├── urls.py                      # User app URL routes
│   └── migrations/                  # Auto-generated migration files
│       ├── __init__.py
│       └── ... (migration files)
│
├── manage.py                        # Django management CLI
├── requirements.txt                 # Python dependencies
├── README.md                        # Project documentation
└── ...                              # Other files like docker, venv, flake8 etc.

```

# Contributing
1. **Fork the repository**
2. **Create a feature branch:**
    ```
   git checkout -b feature-branch
   ```
3. **Commit your changes:**
    ```
   git commit -m "Add feature"
   ```
4. **Push your branch:**
    ```git push origin feature-branch```
5. **Create a Pull Request**
