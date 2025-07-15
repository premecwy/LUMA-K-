from fastapi import FastAPI
from Task.utils.router import router as task_router
from pydantic import BaseModel

app = FastAPI()

app.include_router(task_router)