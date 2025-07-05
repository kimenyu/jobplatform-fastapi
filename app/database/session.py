from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite DB URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./jobboard.db"

# Needed only for SQLite to allow multi-threaded access
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal: each request will get its own session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
