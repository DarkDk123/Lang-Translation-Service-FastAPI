"""
crud.py
---

Contains CRUD operations for tasks, translations on Database.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select
import models


def create_trans_task(
    dbSession: Session, text: str, languages: list[str]
) -> models.TranslationTasks:
    """Create a new translation task"""

    # Create new task
    task = models.TranslationTasks(
        id=0, text="", languages="", status="pending", translation=""
    )

    # Add & commit to database
    dbSession.add(task)
    dbSession.commit()

    return task


def get_task(dbSession: Session, task_id: int):
    """Get a translation task by ID"""

    task = dbSession.execute(
        select(models.TranslationTasks).where(
            models.TranslationTasks.id == task_id
        )  # Using statement.
    )

    return task.first()  # Either None or a single row !


def update_translation_task(
    dbSession: Session, task_id: int, translations: dict[str, str]
):
    """updated a task on completion with final translations"""
    task = dbSession.execute(
        select(models.TranslationTasks).where(models.TranslationTasks.id == task_id)
    ).first()

    # No task found, server error to update!!
    if not task:
        raise Exception("Updating a task that doesn't Exists!!")

    task.translations = translations

    # Save updated task in DB
    dbSession.commit()
    dbSession.refresh(task)  # Refresh current task from DB

    return task
