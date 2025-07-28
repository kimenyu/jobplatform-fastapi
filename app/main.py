from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

from app.api import auth
from app.routes import job, application, review
from app.database.session import engine
from app.database.base import Base

load_dotenv()

# Create all tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI()

@app.get("/")
async def home():
    return {"message": "It is working"}

# app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads") // will change if not using open ai to parse the resumes

# Register routers
app.include_router(auth.router)
app.include_router(job.router)
app.include_router(application.router)
app.include_router(review.router)
