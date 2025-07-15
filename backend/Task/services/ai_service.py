from ai.model_loader import classify_task
from services.task_service import add_task, edit_task, remove_task, check_task
from models import Task
import logging

logging.basicConfig(level=logging.INFO)

def handle_task_by_text(uid: str, task_text: str, task_data: Task = None, task_id: str = None):
    try:
        if not uid or not task_text:
            return {"error": "Missing required uid or task_text"}

        intent = classify_task(task_text)
        logging.info(f"[AI INTENT] '{task_text}' classified as: {intent}")

        if intent == "add":
            if not task_data:
                return {"error": "Task data is required for adding a task"}
            task_id = add_task(uid, task_data)
            return {"success": True, "action": "add", "task_id": task_id}

        elif intent == "edit":
            if not task_data or not task_id:
                return {"error": "Both task_id and task_data are required for editing"}
            edit_task(uid, task_id, task_data)
            return {"success": True, "action": "edit", "task_id": task_id}

        elif intent == "remove":
            if not task_id:
                return {"error": "task_id is required to remove a task"}
            remove_task(uid, task_id)
            return {"success": True, "action": "remove", "task_id": task_id}

        elif intent == "check":
            if not task_id:
                return {"error": "task_id is required to check a task"}
            check_task(uid, task_id)
            return {"success": True, "action": "check", "task_id": task_id}

        else:
            return {"error": f"Unknown action: {intent}"}

    except Exception as e:
        logging.error(f"[ERROR] Failed to process task: {e}")
        return {"error": "Internal server error", "details": str(e)}
