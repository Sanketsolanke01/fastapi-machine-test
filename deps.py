from database import SessionLocal
from fastapi import Depends, HTTPException
from jose import jwt
from models import User

SECRET_KEY = "secret"
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str, db):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = db.query(User).filter(User.id == payload["id"]).first()
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid token")