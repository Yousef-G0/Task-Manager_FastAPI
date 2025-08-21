# Task Manager API (FastAPI + SQLAlchemy + JWT)

A minimal Task Manager REST API with **authentication (JWT)**, **CRUD**, **validation**, and a **SQLite** database (via SQLAlchemy 2.0). Ship it locally with Uvicorn, or deploy to Render.

## Features
- Users: register, login (JWT), get profile
- Tasks: create, read (single/list + pagination + filter by status), update, delete
- Ownership & authorization: users see their own tasks; admins can see all
- SQLite by default; switch DB via `DATABASE_URL`
- OpenAPI docs at `/docs` (Swagger) and `/redoc`

## Tech
- FastAPI, Uvicorn
- SQLAlchemy 2.0 (ORM)
- Pydantic v2
- PyJWT (tokens), passlib (password hashing)

## Project layout
task-manager/
├─ requirements.txt
├─ .gitignore
└─ app/
      ├─ init.py
      ├─ database.py
      ├─ models.py
      ├─ schemas.py
      ├─ auth.py
      └─ main.py


## Prerequisites
- Python **3.10+**
- Git

## Quick start (local)

### Windows PowerShell
```powershell
cd task-manager
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# run
python -m uvicorn app.main:app --reload
```

### MacOS/Linux
```terminal
cd task-manager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# run
uvicorn app.main:app --reload
```
### Open from here 
```http://127.0.0.1:8000/docs```
https://miro.medium.com/v2/resize:fit:1100/format:webp/0*1yRf76ev17TERbVu
