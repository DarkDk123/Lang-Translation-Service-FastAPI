"""
Database.py
---

This file contains the Database initializations.
"""

import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base  # Imported for 'main' file


# Load environment variables
from dotenv import load_dotenv

load_dotenv()


# Create DataBase Engine
# Manages connection to the DB
SQLALCHEMY_DB_URL = os.getenv(
    "SQLALCHEMY_DB_URL", "sqlite:///temp_sqlite.db"
)  # Updated default database
engine = create_engine(SQLALCHEMY_DB_URL)


# Session_maker helps to create multiple temp sessions with given conf.
# Sessions are for executing ORM Queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# This will create new session & close it on each request! (Dependency Injection)
def get_db() -> Generator[Session, None, None]:
    """
    Returns a database session. (Automatically closes with generator)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# For wildcard imports | Not needed, but learning
__all__ = ["engine", "SessionLocal", "get_db", "Base"]
