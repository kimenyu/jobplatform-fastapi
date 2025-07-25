from fastapi import FastAPI
from app.api import auth
from app.routes import job
from app.routes import application
from app.database.session import engine
from app.database.base import Base
from app.models import user
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/docs", StaticFiles(directory="docs", html=True), name="docs")

@app.get("/")
async def home():
    return "It is working"
# Register auth routes
app.include_router(auth.router)
app.include_router(job.router)
app.include_router(application.router)