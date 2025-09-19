from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# For dev: SQLite (switch to PostgreSQL in prod)
SQLALCHEMY_DATABASE_URL = "sqlite:///./feedbacks.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency-style DB session generator"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
