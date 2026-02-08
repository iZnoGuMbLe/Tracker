from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.handlers import tasks

app = FastAPI(title="Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://51.250.6.80"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(tasks.router)
