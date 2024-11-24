from typing import Any, Optional
from celery.result import AsyncResult
from fastapi import APIRouter
from pydantic import BaseModel

class Task(BaseModel):
    task_id:str
    status:str
    result:Optional[Any]


def register_tasks_endpoint(router:APIRouter):
    @router.get("/task-status/{task_id}", summary="ping task", response_description="ping task",status_code=200,response_model=Any)
    async def get_task_status(task_id: str):
        """Check the status of the background task"""
        _task = AsyncResult(task_id)
        task = Task(task_id=_task.id,status=_task.state)
        if task.state == "SUCCESS":
            task.result = task.result
        elif task.state == "PENDING":
            task.result = "Task is still pending"
        elif task.state == "FAILURE":
            task.result = "Task failed"

        return task
