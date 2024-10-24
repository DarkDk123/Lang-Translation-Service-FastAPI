"""
main.py
---

Main FastAPI server (app) file, having all the routes defined.
"""

# ______Imports______
# Currently learning, so no extra (template) imports

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates  # For HTML templates


# Adding Jinja2 templates
templates: Jinja2Templates = Jinja2Templates(directory="templates")  # On given path

# Main app
app = FastAPI()


# ________Routes________
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "message": "Hello World"}
    )
