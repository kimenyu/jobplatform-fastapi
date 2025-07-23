from fastapi import FastAPI
from app.api import auth
from app.routes import job
from app.routes import application
from app.database.session import engine
from app.database.base import Base
from app.models import user  # make sure to import all models here

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def home():
    return "It is working"
# Register auth routes
app.include_router(auth.router)
app.include_router(job.router)
app.include_router(application.router)