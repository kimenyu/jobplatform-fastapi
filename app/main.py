import os
import uuid

from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware

# Routers
from app.api import auth
from app.routes import job, review, userprofile, applicationwithresumeparser
from app.database.session import engine
from app.database.base import Base

from app.config.logging_config import configure_logging
import structlog
import structlog.contextvars

import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

load_dotenv()


Base.metadata.create_all(bind=engine)

configure_logging()
log = structlog.get_logger()

def _bind_ctx(**kwargs):
    for k, v in kwargs.items():
        structlog.contextvars.bind_contextvars(**{k: v})

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        client_ip = request.headers.get("x-forwarded-for", request.client.host)

        _bind_ctx(
            request_id=request_id,
            client_ip=client_ip,
            method=request.method,
            path=request.url.path,
        )

        log.info("http.request.start")

        try:
            if request.method in {"POST", "PUT", "PATCH"}:
                body = await request.body()
                if body and len(body) <= 1024:
                    log.info("http.request.body_sample", size=len(body))
        except Exception:
            pass

        response = await call_next(request)
        response.headers["x-request-id"] = request_id
        log.info("http.request.end", status_code=response.status_code)
        return response

async def identifier(request: Request) -> str:

    user_id = request.headers.get("x-user-id")  # example placeholder
    if user_id:
        return f"user:{user_id}"
    ip = request.headers.get("x-forwarded-for", request.client.host)
    return f"ip:{ip}"

async def init_rate_limit():
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    r = redis.from_url(redis_url, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(r, identifier=identifier)

app = FastAPI(
    dependencies=[Depends(RateLimiter(times=120, seconds=60))]
)

# Middlewares
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "your-secret-key-here")  # Use a strong secret key
)

# Startup hooks
@app.on_event("startup")
async def on_startup():
    await init_rate_limit()
    log.info("app.startup.complete")


@app.get("/test")
async def home():
    return {"message": "It is working"}

app.include_router(
    auth.router,
    dependencies=[Depends(RateLimiter(times=10, seconds=60))]
)

app.include_router(job.router)
app.include_router(review.router)
app.include_router(userprofile.router)

app.include_router(
    applicationwithresumeparser.router,
    dependencies=[Depends(RateLimiter(times=60, seconds=60))]
)
