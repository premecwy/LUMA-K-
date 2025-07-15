from fastapi import APIRouter
from pydantic import BaseModel
import sys
import os
sys.path.append(os.path.dirname(__file__))

from llm_search.llm_core import ask_llm_raw
from llm_search.search_core import search_google
from llm_search.scrape_core import scrape_text


router = APIRouter()

# --- LLM Endpoint ---
class LLMRequest(BaseModel):
    prompt: str

@router.post("/llm_core")
def route_llm(req: LLMRequest):
    result = ask_llm_raw(req.prompt)
    return {"response": result}

# --- Google Search ---
class GoogleSearchRequest(BaseModel):
    query: str
    api_key: str
    num_results: int = 1

@router.post("/search_google")
def route_search_google(req: GoogleSearchRequest):
    links = search_google(req.query, req.api_key, req.num_results)
    return {"links": links}

# --- Scrape URL ---
class URLRequest(BaseModel):
    url: str

@router.post("/scrape")
def route_scrape(req: URLRequest):
    content = scrape_text(req.url)
    return {"content": content[:1000]}  # ตัดข้อความให้สั้น, ปรับตามต้องการ

