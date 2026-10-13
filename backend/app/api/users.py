from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import sqlite3
from app.db import get_db
from app.api.auth_utils import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/users", tags=["users"])

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(user: UserCreate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (user.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email already registered")
        
    hashed_pwd = get_password_hash(user.password)
    
    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (user.name, user.email, hashed_pwd)
    )
    db.commit()
    user_id = cursor.lastrowid
    
    # Initialize settings
    cursor.execute(
        "INSERT INTO settings (user_id) VALUES (?)",
        (user_id,)
    )
    db.commit()
    
    token = create_access_token(data={"sub": str(user_id)})
    return {"access_token": token, "token_type": "bearer", "user": {"id": user_id, "name": user.name, "email": user.email}}

@router.post("/login")
def login(user: UserLogin, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, name, email, password_hash FROM users WHERE email = ?", (user.email,))
    db_user = cursor.fetchone()
    
    if not db_user or not verify_password(user.password, db_user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
        
    token = create_access_token(data={"sub": str(db_user["id"])})
    return {"access_token": token, "token_type": "bearer", "user": {"id": db_user["id"], "name": db_user["name"], "email": db_user["email"]}}

@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    return current_user
