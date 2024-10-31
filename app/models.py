"""
models.py
---

Contains DataBase models (tables) declared as Classes (declarative base (preferred)).

Read more on : [Declarative Vs Imperative](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#declarative-vs-imperative-forms)
"""

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, JSON

# Base class to inherit models.
Base = declarative_base()


class TranslationTasks(Base):
    __tablename__ = "translation_tasks"

    id = Column(Integer, primary_key=True, nullable=False)
    text = Column(Text, nullable=False)
    languages = Column(String, nullable=False)
    status = Column(String, default="pending")
    translation: Column[dict] = Column(JSON, default={})

    # SQLModel ORM is an extension of SQLAlchemy ORM
    # Provides better type support with Pydantic. I read a lot through this...
    # https://sqlmodel.tiangolo.com/
