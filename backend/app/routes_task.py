from fastapi import APIRouter
from celery.result import AsyncResult
from backend.app.celery_app import celery_app

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/{task_id}")
def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)

    response = {
        "task_id": task_id,
        "state": result.state,
        "info": result.info if result.info else None,
    }

    return response
