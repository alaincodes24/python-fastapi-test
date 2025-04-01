from fastapi import APIRouter, Depends, HTTPException
from app.schemas import UserCreate, UserOut
from app.services import create_user
from app.auth import create_access_token, verify_password
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User

router = APIRouter()

def session_get_local() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", response_model=str)
def signup(user: UserCreate, db: Session = Depends(session_get_local)):
    db_user = create_user(db, user)
    access_token = create_access_token(data={"sub": db_user.email})
    return access_token

@router.post("/login", response_model=str) 
def login(user: UserCreate, db: Session = Depends(session_get_local)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user.email})
    return access_token
