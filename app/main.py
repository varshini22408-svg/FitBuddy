from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routes import router

app = FastAPI(title="FitBuddy")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)