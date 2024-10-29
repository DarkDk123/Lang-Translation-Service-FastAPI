"""
Database.py
---

This file contains the Database initializations.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Load environment variables
from dotenv import load_dotenv

load_dotenv()


# Create DataBase Engine
# Manages connection to the DB
SQLALCHEMY_DB_URL = os.getenv("SQLALCHEMY_DB_URL", "")
engine = create_engine(SQLALCHEMY_DB_URL)


# Session_maker helps to create multiple temp sessions with given conf.
# Sessions are for executing ORM Queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# For wildcard imports | Not needed, but learning
__all__ = ["engine", "SessionLocal"]
