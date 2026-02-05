from fastapi import FastAPI
from app.handlers import tasks

app = FastAPI(title="Tracker API")

app.include_router(tasks.router)
