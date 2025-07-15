from fastapi import FastAPI

from speech.utils.router import router as speech_router
from llm_search.utils.router import router as llm_router

app = FastAPI()

app.include_router(llm_router, prefix="/llm", tags=["LLM + Search"])
app.include_router(speech_router, prefix="/speech", tags=["Speech"])