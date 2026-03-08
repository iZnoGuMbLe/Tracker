from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from app.handlers import tasks,auth
from app.models import UserModel,TaskModel

app = FastAPI(title="Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
	"http://localhost:3000",
	"https://dailytracker.ru",
	"https://www.dailytracker.ru",
	"http://localhost:5173"
	],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)


app.include_router(auth.router)
app.include_router(tasks.router)

@app.get("/")
async def root():
    return {
        "message": "Tracker API",
        "version": "1.0.0",
        "docs": "/docs"
    }
