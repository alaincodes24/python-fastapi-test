from sqlalchemy.orm import Session
from app.models import User, Post
from app.schemas import UserCreate, PostCreate
from app.auth import get_password_hash

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_post(db: Session, post: PostCreate, user_id: int):
    db_post = Post(text=post.text, owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Post).filter(Post.owner_id == user_id).offset(skip).limit(limit).all()
