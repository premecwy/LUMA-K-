from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

from llm_core import ask_llm_raw
class LLMRequest(BaseModel):
    prompt: str

@app.post("/llm_core")
def route_llm(req: LLMRequest):
    result = ask_llm_raw(req.prompt)
    return {"response": result}

from search_core import search_google
class GoogleSearchRequest(BaseModel):
    query: str
    api_key: str
    num_results: int = 1

@app.post("/search_google")
def route_search_google(req: GoogleSearchRequest):
    links = search_google(req.query, req.api_key, req.num_results)
    return {"links": links}

from controller import ask_with_cli_and_fallback
class PromptRequest(BaseModel):
    prompt: str
    api_key: str

@app.post("/ask")
def route_ask(req: PromptRequest):
    if not req.api_key:
        return {"error": "ต้องระบุ api_key ของ Google Search API"}
    answer = ask_with_cli_and_fallback(req.prompt, req.api_key)
    return {"answer": answer}

from scrape_core import scrape_text
class URLRequest(BaseModel):
    url: str
@app.post("/scrape")
def route_scrape(req: URLRequest):
    content = scrape_text(req.url)
    return {"content": content[:1000]}  # ตัดข้อความให้สั้น, ปรับตามต้องการ
