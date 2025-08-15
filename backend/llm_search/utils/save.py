import os
from fastapi import APIRouter
from pydantic import BaseModel
import logging
from dotenv import load_dotenv

from ..llm_core import ask_llm_raw
from ..search_core import search_google
from ..scrape_core import scrape_text

router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FillFormPOC")

# โหลด environment variables
load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

class PredictRequest(BaseModel):
    text: str

@router.post("/llm_search")
async def llm_search(request: PredictRequest):
    query = request.text
    logger.info(f"[REQUEST] Prompt: {query}")

    response = ask_llm_raw(query)

    # === Intent Logic ===
    if ("แพลน" in query or "เที่ยว" in query) and ("search" in query or "หาข้อมูล" in query):
        intents = ["Plan", "Search"]
    elif "แพลน" in query or "เที่ยว" in query:
        intents = ["Plan"]
    elif "search" in query or "หาข้อมูล" in query:
        intents = ["Search"]
    elif any(kw in response for kw in ["ไม่รู้", "ไม่มั่นใจ", "ไม่มีข้อมูล", "ไม่พบ", "ตรวจสอบ"]):
        intents = ["GoogleSearch"]
    else:
        intents = ["Search"]

    result = {
        "prompt": query,
        "intent": intents,
        "decoration_input": {
            "input": query,
            "response": response
        },
        "massage": response
    }

    # 🔹 แก้ไขตรงนี้
    links = []
    if "GoogleSearch" in intents:
        links = search_google(query, api_key=SERPAPI_KEY, num_results=1)

    if links:
        scraped_content = scrape_text(links[0])
        summary_prompt = f"""
คุณคือผู้ช่วยที่สรุปข้อมูลจากเว็บไซต์

คำถามของผู้ใช้: "{query}"

เนื้อหาที่ดึงมา:
{scraped_content}

กรุณาสรุปคำตอบตามคำถามของผู้ใช้โดยตรง 
ให้กระชับ ไม่เกิน 3 ประโยค 
ถ้าในเนื้อหาที่ให้มาไม่มีข้อมูลที่ตอบคำถามได้ 
ให้ตอบว่า "ไม่พบข้อมูลที่เกี่ยวข้อง"
"""
        summarized = ask_llm_raw(summary_prompt)
        result["decoration_input"]["response"] = summarized
        result["decoration_input"]["source"] = links[0]
        result["massage"] = summarized

    logger.info(f"[RESPONSE] {result}")
    return result

from fastapi import APIRouter
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from ..llm_core import ask_llm_raw
from ..search_core import search_google
from ..scrape_core import scrape_text

# โหลดค่า API key จาก .env
load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")

router = APIRouter()

# Schema สำหรับรับ input
class LLMRequest(BaseModel):
    prompt: str

@router.post("/llm_core")
def llm_core(req: LLMRequest):
    query = req.prompt
    response = ask_llm_raw(query)

    print(f"[DEBUG] LLM response: {response}")  # Debug log

    # --- Fallback ถ้า LLM ไม่มั่นใจ ---
    if any(kw in response for kw in ["ไม่รู้", "ไม่มั่นใจ", "ไม่มีข้อมูล", "ไม่พบ", "ตรวจสอบ"]):
        print("[DEBUG] Trigger fallback → Google Search")
        links = search_google(query, api_key=SERPAPI_KEY, num_results=1)
        if links:
            scraped = scrape_text(links[0])
            return {
            "response": f"🤔 LLM ไม่มั่นใจ\n🌐 Google: {scraped[:500]}...",
            "source": links[0]
            }
        else:
            return {
                "response": "❌ ไม่สามารถหาข้อมูลจาก Google ได้",
                "source": None
            }

