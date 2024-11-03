"""
util.py
---

Utility functions for the app having API integrations for the translation task.
"""

from crud import update_translation_task
from sqlalchemy.orm import Session
from language_map import LANGUAGE_MAPPING
from googletrans import Translator

# Initialize Google translator
translator = Translator()


async def perform_trans(task_id, text: str, languages: list[str], dbSession: Session):
    # Get the translations
    translations = {
        language: await _translate(text, language) for language in languages
    }

    # Update translations in the Database
    update_translation_task(dbSession, task_id=task_id, translations=translations)


# Using Google Translate API
async def _translate(text: str, language: str) -> str:
    try:
        # Get the language code from our mapping
        target_lang = LANGUAGE_MAPPING[language]

        # Translate using Google Translate
        result = translator.translate(text, dest=target_lang.lower())

        return result.text
    except Exception as e:
        print(f"Error occurred while translating text: {e}")
        return "Could not translate this text"


def invalid_languages(languages: list[str]):
    global LANGUAGE_MAPPING
    return [lang for lang in languages if lang not in LANGUAGE_MAPPING.keys()]
