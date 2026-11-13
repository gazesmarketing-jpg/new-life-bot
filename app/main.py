"""FastAPI application for the staff web dashboard."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app import database

# ------------------------------------------------------------------ #
#  Create app
# ------------------------------------------------------------------ #
app = FastAPI(title="New Life Training Center - Staff Dashboard")

# CORS for dashboard (allow local dev origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates + static files
templates_dir = Path(__file__).parent / "templates"
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=str(templates_dir))

# Database init on startup
@app.on_event("startup")
async def startup():
    await database.init_db()


@app.on_event("shutdown")
async def shutdown():
    # In production, close engine connections here
    pass


# ------------------------------------------------------------------ #
#  Health / readiness
# ------------------------------------------------------------------ #
@app.get("/health", tags=["system"])
async def health():
    return {"status": "ok", "service": "new-life-dashboard"}


# ------------------------------------------------------------------ #
#  Redirects for clean URLs
# ------------------------------------------------------------------ #
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/dashboard")


# ------------------------------------------------------------------ #
#  Pages
# ------------------------------------------------------------------ #
@app.get("/dashboard", response_class=HTMLResponse, tags=["dashboard"])
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/login", response_class=HTMLResponse, tags=["auth"])
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# 404 fallback
@app.get("/{full_path:path}", response_class=HTMLResponse, include_in_schema=False)
async def spa_fallback(request: Request, full_path: str):
    return templates.TemplateResponse("index.html", {"request": request})
