from fastapi import APIRouter, Depends, HTTPException, Request
from app.schemas import PostCreate, PostOut
from app.services import create_post, get_posts
from app.auth import get_current_user
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User 

router = APIRouter()


def get_session_local() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=dict)
async def create_post_route(
    post: PostCreate,
    db: Session = Depends(get_session_local),
    current_user: User = Depends(get_current_user)
):
    if len(str(post.text).encode('utf-8')) > 1024 * 1024:  
        raise HTTPException(status_code=413, detail="Payload too large. The text exceeds 1 MB.")
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    new_post = create_post(db, post, current_user.id)
    return {"postID": new_post.id}

@router.get("/", response_model=list[PostOut])
def get_posts_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_session_local), current_user: User = Depends(get_current_user)):
    return get_posts(db, current_user.id, skip=skip, limit=limit)
