from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from typing import List, Optional

from app.schemas.task_schema import TaskCreate,TaskUpdate,TaskResponse
from app.database.session import get_session
from app.repositories.task import TaskRepository
from app.service.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])

def get_task_service(session: AsyncSession = Depends(get_session)) -> TaskService:
    repository = TaskRepository(session)
    return TaskService(repository)

@router.post('/', response_model=TaskResponse)
async def create_task(task_data:TaskCreate, service: TaskService = Depends(get_task_service)):
    return await service.create_task(task_data)

@router.get('/', response_model=List[TaskResponse])
async def get_tasks_list(service: TaskService = Depends(get_task_service)):
    return await service.get_all_tasks()

@router.get("/by-date/{target_date}", response_model=list[TaskResponse])
async def get_task_by_date(
    target_date: date,
    service: TaskService = Depends(get_task_service)
):
    return await service.get_tasks_by_date(target_date=target_date)

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    task = await service.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task


@router.patch('/{task_id}', response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    service: TaskService = Depends(get_task_service)
):
    task = await service.update_task(task_id, task_data)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task

@router.post("/{task_id}/complete", response_model=TaskResponse)
async def mark_task_as_done(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    task = await service.mark_as_done(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task


@router.post("/{task_id}/incomplete", response_model=TaskResponse)
async def mark_task_as_incomplete(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    task = await service.mark_as_undone(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    deleted = await service.delete_task(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

