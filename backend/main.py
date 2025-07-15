from fastapi import FastAPI
from pydantic import BaseModel

# รวม router ตาม module
from speech.utils.router import router as speech_router
from llm_search.utils.router import router as llm_router
from Task.utils.router import router as task_router  # ถ้ามี router รวมบางส่วนใน Task

app = FastAPI()

# รวม router ทั้งหมด
app.include_router(llm_router, prefix="/llm", tags=["LLM + Search"])
app.include_router(speech_router, prefix="/speech", tags=["Speech"])
app.include_router(task_router, prefix="/task", tags=["Task"])  # จะใส่ prefix หรือไม่ก็ได้
