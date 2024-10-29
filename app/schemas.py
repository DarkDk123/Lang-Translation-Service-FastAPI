"""
Schemas
---

Declared Schemas for the api requests & Response formats.
"""

from pydantic import BaseModel


class TranslationRequest(BaseModel):
    """Request schema for /translate endpoint."""

    text: str
    languages: list[str]


class TaskResponse(BaseModel):
    """Response schema for task creation."""

    task_id: int


class TranslationStatusResponse(BaseModel):
    """Response schema for task status"""

    task_id: int
    status: str
    translations: dict[str, str]
