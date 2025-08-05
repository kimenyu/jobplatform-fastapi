from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

from app.api import auth
from app.routes import job, review, userprofile, applicationwithresumeparser
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


# Register routers
app.include_router(auth.router)
app.include_router(job.router)
app.include_router(review.router)
app.include_router(userprofile.router)
app.include_router(applicationwithresumeparser.router)
