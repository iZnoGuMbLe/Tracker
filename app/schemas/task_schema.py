from pydantic import BaseModel, Field
from datetime import datetime

class TaskCreate(BaseModel):
    """" здесь про данные, которые клиент
    отправляет на создание или редактирования"""

    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    due_date: datetime | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_done: bool | None = None
    due_date: datetime | None = None

class TaskResponse(BaseModel):
    """" здесь про данные,
    которые сервер возвращает клиенту."""

    id: int
    title: str
    description: str | None
    is_done: bool
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None
    due_date: datetime | None

    class Config:
        orm_mode = True
        from_attributes = True

