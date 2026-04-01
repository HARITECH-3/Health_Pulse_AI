from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
import smtplib
import secrets
from email.message import EmailMessage
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from bson import ObjectId

from app.db import get_db
from app.schemas import UserCreate, UserResponse, Token, ForgotPasswordRequest, ResetPasswordRequest, DirectResetPasswordRequest
from app.config import settings
from pymongo.database import Database

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Database = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.users.find_one({"username": username})
    if user is None:
        raise credentials_exception
    user["id"] = str(user["_id"])
    return user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def get_user_by_email(db: Database, email: str):
    return db.users.find_one({"email": email})

def get_user_by_username(db: Database, username: str):
    return db.users.find_one({"username": username})

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: Database = Depends(get_db)):
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    
    hashed_password = get_password_hash(user.password)
    user_doc = {
        "email": user.email,
        "username": user.username,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow(),
        "is_active": True
    }
    result = db.users.insert_one(user_doc)
    
    # ID mapping
    user_doc["id"] = str(result.inserted_id)
    return user_doc

from pydantic import BaseModel
class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login", response_model=Token)
async def login_user(payload: LoginRequest, db: Database = Depends(get_db)):
    # Check by both email and username since user might provide either
    db_user = db.users.find_one({"$or": [{"email": payload.email}, {"username": payload.email}]})
    
    if not db_user or not verify_password(payload.password, db_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # Track the last login time in MongoDB Atlas
    db.users.update_one(
        {"_id": db_user["_id"]},
        {"$set": {"last_login": datetime.utcnow()}}
    )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user["username"]}, 
        expires_delta=access_token_expires
    )
    # Also return the user id so frontend can save it for chat!
    return {"access_token": access_token, "token_type": "bearer", "user_id": str(db_user["_id"])}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user

@router.get("/", response_model=List[UserResponse])
async def get_users(skip: int = 0, limit: int = 100, db: Database = Depends(get_db)):
    users = list(db.users.find().skip(skip).limit(limit))
    for u in users:
        u["id"] = str(u["_id"])
    return users

@router.post("/reset-password-direct")
async def reset_password_direct(
    request: DirectResetPasswordRequest,
    db: Database = Depends(get_db)
):
    user = get_user_by_email(db, request.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    hashed_password = get_password_hash(request.new_password)
    db.users.update_one({"_id": user["_id"]}, {"$set": {"hashed_password": hashed_password}})
    
    return {"msg": "Password successfully reset"}
