"""
util.py
---

Utility functions for the app having API integrations for the translation task.
"""

from crud import update_translation_task
from sqlalchemy.orm import Session
from language_map import LANGUAGE_MAPPING



async def perform_trans(task_id, text: str, languages: list[str], dbSession: Session):
    # Get the translations
    translations = {
        language: await _translate(text, language) for language in languages
    }

    # Update translations in the Database
    update_translation_task(dbSession, task_id=task_id, translations=translations)


async def _translate(text: str, language: str) -> str:
    # TODO: Hugging Face model for translation
    try:
        return ""
    except Exception as e:
        print(f"Error occurred while translating text: {e}")
    finally:
        return ""


def invalid_languages(languages: list[str]):
    global LANGUAGE_MAPPING
    return [lang for lang in languages if lang not in LANGUAGE_MAPPING.keys()]
