from firebase_config import db
from models import Task
from datetime import datetime
from google.cloud.exceptions import NotFound
import logging

logging.basicConfig(level=logging.INFO)

def add_task(uid: str, task: Task) -> str:
    try:
        doc_ref = db.collection("users").document(uid).collection("tasks").document()
        task_data = task.dict()
        task_data["created_at"] = datetime.utcnow()
        task_data["updated_at"] = datetime.utcnow()
        doc_ref.set(task_data)
        logging.info(f"[ADD] Task created for user '{uid}' with ID: {doc_ref.id}")
        return doc_ref.id
    except Exception as e:
        logging.error(f"[ERROR] Failed to add task for user {uid}: {e}")
        raise

def edit_task(uid: str, task_id: str, task: Task):
    try:
        ref = db.collection("users").document(uid).collection("tasks").document(task_id)
        updated_data = task.dict()
        updated_data["updated_at"] = datetime.utcnow()
        ref.update(updated_data)
        logging.info(f"[EDIT] Task {task_id} updated for user '{uid}'")
    except NotFound:
        logging.error(f"[ERROR] Task {task_id} not found for user '{uid}'")
        raise
    except Exception as e:
        logging.error(f"[ERROR] Failed to edit task {task_id} for user {uid}: {e}")
        raise

def remove_task(uid: str, task_id: str):
    try:
        ref = db.collection("users").document(uid).collection("tasks").document(task_id)
        ref.delete()
        logging.info(f"[REMOVE] Task {task_id} deleted for user '{uid}'")
    except Exception as e:
        logging.error(f"[ERROR] Failed to delete task {task_id} for user {uid}: {e}")
        raise

def check_task(uid: str, task_id: str):
    try:
        ref = db.collection("users").document(uid).collection("tasks").document(task_id)
        ref.update({
            "complete": True,
            "updated_at": datetime.utcnow()
        })
        logging.info(f"[CHECK] Task {task_id} marked complete for user '{uid}'")
    except Exception as e:
        logging.error(f"[ERROR] Failed to mark task {task_id} complete for user {uid}: {e}")
        raise
