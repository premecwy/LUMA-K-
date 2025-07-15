from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os
sys.path.append(os.path.dirname(__file__))

app = FastAPI()

from llm_search.llm_core import ask_llm_raw
class LLMRequest(BaseModel):
    prompt: str

@app.post("/llm_core")
def route_llm(req: LLMRequest):
    result = ask_llm_raw(req.prompt)
    return {"response": result}

from llm_search.search_core import search_google
class GoogleSearchRequest(BaseModel):
    query: str
    api_key: str
    num_results: int = 1

@app.post("/search_google")
def route_search_google(req: GoogleSearchRequest):
    links = search_google(req.query, req.api_key, req.num_results)
    return {"links": links}

from llm_search.scrape_core import scrape_text
class URLRequest(BaseModel):
    url: str
@app.post("/scrape")
def route_scrape(req: URLRequest):
    content = scrape_text(req.url)
    return {"content": content[:1000]}  # ตัดข้อความให้สั้น, ปรับตามต้องการ

class RecordRequest(BaseModel):
    duration: int = 5
    filename: str = "thai_input.wav"

class TranscribeRequest(BaseModel):
    filename: str = "thai_input.wav"
    model_size: str = "small"
    device: str = "cpu"
    lang: str = "th"

from speech.stt_core import record_audio
@app.post("/record")
def route_record(req: RecordRequest):
    filename = record_audio(req.filename, req.duration)
    return {"filename": filename}

from speech.stt_core import transcribe_audio
@app.post("/transcribe")
def route_transcribe(req: TranscribeRequest):
    text = transcribe_audio(
        filename=req.filename,
        model_size=req.model_size,
        device=req.device,
        lang=req.lang
    )
    return {"transcription": text}

class TTSRequest(BaseModel):
    text: str
    output_path: str = "thai_tts_output.wav"
    length_scale: float = 1.0

from speech.tts_core import generate_khanomtan_tts
@app.post("/tts")
def tts_api(req: TTSRequest):
    path = generate_khanomtan_tts(req.text, req.output_path, req.length_scale)
    return {"path": path}
