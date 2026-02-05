from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import datetime, date,timezone
from app.models.task import TaskModel
from app.schemas.task_schema import TaskCreate, TaskUpdate

class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task_data: TaskCreate) -> TaskModel:
        task = TaskModel(**task_data.model_dump())
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get_task_by_id(self, task_id: int) -> TaskModel | None:
        result = await self.session.execute(
            select(TaskModel).where(TaskModel.id == task_id)
        )
        return result.scalar_one_or_none()

    async def get_tasks_list(self) -> list[TaskModel]:
        result = await self.session.execute(select(TaskModel))
        return list(result.scalars().all())

    async def get_task_by_date(self, target_date: date) -> list[TaskModel]:
        """Получить задачи, созданные в конкретный день"""
        start_of_day = datetime.combine(target_date, datetime.min.time())
        end_of_day = datetime.combine(target_date, datetime.max.time())

        result = await self.session.execute(
            select(TaskModel).where(
                and_(
                    TaskModel.created_at >= start_of_day,
                    TaskModel.created_at <= end_of_day
                )
            )
        )
        return list(result.scalars().all())

    async def update(self, task_id: int, task_data: TaskUpdate) -> TaskModel | None:
        task = await self.get_task_by_id(task_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)

        if 'is_done' in update_data and update_data['is_done']:
            task.completed_at = datetime.now(timezone.utc)
        elif 'is_done' in update_data and not update_data['is_done']:
            task.completed_at = None

        for key, value in update_data.items():
            setattr(task, key, value)

        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete(self, task_id: int) -> bool:
        task = await self.get_task_by_id(task_id)
        if not task:
            return False

        await self.session.delete(task)
        await self.session.commit()
        return True
