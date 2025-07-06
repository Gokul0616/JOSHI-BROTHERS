from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

# Create admin app
admin_app = FastAPI()

# Mount static files for admin panel
admin_app.mount("/static", StaticFiles(directory="admin_static"), name="static")

# Templates
templates = Jinja2Templates(directory="admin_templates")

@admin_app.get("/", response_class=HTMLResponse)
async def admin_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@admin_app.get("/{path:path}", response_class=HTMLResponse)
async def admin_catch_all(request: Request, path: str):
    return templates.TemplateResponse("index.html", {"request": request})