from fastapi import FastAPI
from app.routes import auth_routes, post_routes

app = FastAPI()

app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(post_routes.router, prefix="/posts", tags=["posts"])

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
    