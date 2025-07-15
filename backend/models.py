from pydantic import BaseModel
from typing import Optional

class Task(BaseModel):
    task_id: Optional[str] = None
    task_detail: str
    task_description: Optional[str] = None
    due_date: Optional[str] = None
    complete: Optional[bool] = False
    priority: Optional[int] = 0
