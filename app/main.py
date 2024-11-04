"""
main.py
---

Main FastAPI server (app) file, having all the routes defined.
"""

# ______Imports______
# Currently learning, so no extra (template) imports

from typing import Annotated
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, BackgroundTasks, Depends
from fastapi.responses import HTMLResponse
from fastapi.exceptions import HTTPException

from fastapi.templating import Jinja2Templates  # For HTML templates
from fastapi.middleware.cors import CORSMiddleware

from models import TranslationTasks
from schemas import TranslationRequest, TaskResponse, TranslationStatusResponse
from database import get_db, Base, engine, Session

import crud
from util import perform_trans, invalid_languages
from language_map import LANGUAGE_MAPPING
from datetime import datetime

# Adding Jinja2 templates
templates: Jinja2Templates = Jinja2Templates(directory="templates")  # On given path


# Creating lifespan function!
# For creating db tables at startup only!
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield Base.metadata.create_all(engine)  # Create tables if not exists


# Main app
app = FastAPI(lifespan=lifespan)


# ________Routes________
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "languages": LANGUAGE_MAPPING.keys(),
            "date": datetime.now().strftime("%d %B %Y"),
        },
    )


@app.post("/translate", response_model=TaskResponse)
async def translate(
    request: TranslationRequest,
    dbSession: Annotated[Session, Depends(get_db)],
    bg_tasks: BackgroundTasks,
):

    # Convert languages to lowercase
    request.languages = [lang.lower() for lang in request.languages]

    # Check valid languages
    if inv_lang := invalid_languages(request.languages):
        raise HTTPException(
            status_code=400,
            detail={"msg": "Invalid languages", "invalid_languages": inv_lang},
        )

    # Create new task
    task: TranslationTasks = crud.create_trans_task(
        dbSession, request.text, request.languages
    )

    # perform translation in background
    bg_tasks.add_task(
        perform_trans, task.id, request.text, request.languages, dbSession
    )

    return {"task_id": task.id}


@app.get("/translate/status/{task_id}", response_model=TranslationStatusResponse)
async def get_content_status(
    task_id: int,
    dbSession: Annotated[Session, Depends(get_db)],
):
    # Get task from Database
    task = crud.get_task(dbSession, task_id)

    # No task found, server error to update!!
    if not task:
        raise HTTPException(
            status_code=404, detail="You're referring to a Task that doesn't Exists!!"
        )

    # This will get truncated to response schema
    return {
        "task_id": task.id,
        "status": task.status,
        "text": task.text,
        "translations": task.translation,
    }


# Enable CORS mainly for development.
app.add_middleware(
    CORSMiddleware,
    # These Allows a lot!
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
