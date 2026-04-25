# from __future__ import annotations

# from typing import Generator

# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session, sessionmaker

# from .settings import get_settings

# # Get settings and create engine
# settings = get_settings()
# engine = create_engine(
#     settings.database_url,
#     pool_pre_ping=True,  # Helps with connection reliability
# )

# # Create session factory
# SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# def get_db() -> Generator[Session, None, None]:
#     """Dependency for getting database sessions"""
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .settings import settings

# Create engine
engine = create_engine(settings.DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

def get_db():
    """Dependency for getting database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()