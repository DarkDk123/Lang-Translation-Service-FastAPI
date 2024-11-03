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
        # Language list as string
        text=text,
        languages=",".join(languages),
        status="pending",
        translation={},
    )

    # Add & commit to database
    dbSession.add(task)
    dbSession.commit()

    return task


def get_task(dbSession: Session, task_id: int):
    """Get a translation task by ID"""

    rows = dbSession.execute(
        select(models.TranslationTasks).where(
            models.TranslationTasks.id == task_id
        )  # Using statement.
    ).first()

    # If result row exits
    if rows:
        # No need to convert lang str to list.
        # Return direct results from DB
        return rows[0]

    return None  # No Task !


def update_translation_task(
    dbSession: Session, task_id: int, translations: dict[str, str]
):
    """updated a task on completion with final translations"""

    rows = dbSession.execute(
        select(models.TranslationTasks).where(models.TranslationTasks.id == task_id)
    ).first()

    # No task found, server error to update!!
    if not rows:
        raise Exception("Updating a task that doesn't Exists!!")

    
    task = rows[0]
    task.translation = translations
    task.status = "completed"

    # Save updated task in DB
    dbSession.commit()
    dbSession.refresh(task)  # Refresh current task from DB

    return task
