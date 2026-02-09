from datetime import date
from app.repositories.task import TaskRepository
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse

class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def create_task(self, task_data: TaskCreate, user_id: int) -> TaskResponse:
        task = await self.repository.create(task_data,user_id=user_id)
        return TaskResponse.model_validate(task)

    async def get_task(self, task_id: int, user_id:int) -> TaskResponse | None:
        task = await self.repository.get_task_by_id(task_id,user_id=user_id)
        if not task:
            return None
        return TaskResponse.model_validate(task)

    async def get_all_tasks(self, user_id: int) -> list[TaskResponse]:
        tasks = await self.repository.get_tasks_list(user_id=user_id)
        return [TaskResponse.model_validate(task) for task in tasks]

    async def get_tasks_by_date(self, target_date: date, user_id:int) -> list[TaskResponse]:
        tasks = await self.repository.get_task_by_date(target_date,user_id=user_id)
        return [TaskResponse.model_validate(task) for task in tasks]

    async def update_task(self, task_id: int, task_data: TaskUpdate, user_id: int) -> TaskResponse | None:
        task = await self.repository.update(task_id, task_data, user_id=user_id)
        if not task:
            return None
        return TaskResponse.model_validate(task)

    async def delete_task(self, task_id: int,user_id:int) -> bool:
        return await self.repository.delete(task_id, user_id=user_id)

    async def mark_as_done(self, task_id: int, user_id:int) -> TaskResponse | None:
        return await self.update_task(task_id, TaskUpdate(is_done=True),user_id=user_id)

    async def mark_as_undone(self, task_id: int, user_id:int) -> TaskResponse | None:
        return await self.update_task(task_id, TaskUpdate(is_done=False),user_id=user_id)