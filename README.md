
# FastAPI Machine Test

##Tech Stack
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT Authentication

## Setup Instructions

### 1. Clone repo
git clone https://github.com/your-username/fastapi-machine-test.git

### 2. Install dependencies
pip install -r requirements.txt

### 3. Setup Database
Update DATABASE_URL in database.py

### 4. Run server
uvicorn main:app --reload

---

## Authentication
Use token from login API in headers:
Authorization: Bearer <token>

---

## API Endpoints

### User
- POST /users/
- POST /auth/login
- GET /users/

### Client
- POST /clients/
- GET /clients/
- GET /clients/{id}
- PUT /clients/{id}
- DELETE /clients/{id}

### Project
- POST /projects/
- GET /projects/
- DELETE /projects/{id}

---

## Testing
Use Swagger:
http://127.0.0.1:8000/docs
