from fastapi import APIRouter
from services.ai_service import handle_task_by_text
from models import Task

router = APIRouter()

@router.post("/analyze-task")
def analyze_and_execute(uid: str, task_text: str, task: Task = None, task_id: str = None):
    return handle_task_by_text(uid, task_text, task, task_id)
