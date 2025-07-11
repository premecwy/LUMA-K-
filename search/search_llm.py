import os
import sys
import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
from dotenv import load_dotenv
from llama_cpp import Llama
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# === Models ===
class PromptRequest(BaseModel):
    prompt: str
    api_key: str = None

# === โหลดค่า .env ===
load_dotenv()

# === Trigger ที่บอกว่า LLM ตอบแบบไม่รู้ ===
FALLBACK_TRIGGERS = [
    "ฉันไม่สามารถตรวจสอบสภาพอากาศ",
    "ฉันเป็นโปรแกรม AI ที่ไม่มีการเชื่อมต่ออินเทอร์เน็ต",
    "คุณสามารถตรวจสอบสภาพอากาศได้จาก",
    "ไม่มีข้อมูล",
    "ไม่สามารถตอบ"
]

# === โหลด Llama model (แทน llama-cli) ===
llm = Llama(
    model_path="./llama.cpp/build/models/openthaigpt/openthaigpt1.5-7B-instruct-Q4KM.gguf",
    n_ctx=4096,
    n_threads=8,
    n_batch=512,
    use_mlock=True,
    rope_freq_base=1000000.0,        # ตรงกับ metadata
    chat_format="qwen",              # ใช้ template เดียวกับ CLI
    verbose=False,                   # ให้เงียบเหมือน CLI
    escape=True,                     # ป้องกันบั๊ก input ภาษาไทยค้าง
)

def ask_llm_raw(prompt: str) -> str:
    output = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": "คุณคือผู้ช่วยตอบคำถามที่ฉลาดและซื่อสัตย์"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        top_p=0.95,
        top_k=40,
        max_tokens=512,
        repeat_penalty=1.1,
    )
    return output['choices'][0]['message']['content']

# === เช็คว่า LLM ตอบแบบ fallback หรือมั่ว ===
def is_llm_uncertain(text: str) -> bool:
    return any(phrase in text for phrase in FALLBACK_TRIGGERS)

# === ดึงข้อความจากเว็บ ===
def scrape_text(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text(separator=" ", strip=True)
    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        return ""

# === ใช้ Google Search API ===
def search_google(query, api_key, num_results=1):
    try:
        search = GoogleSearch({
            "q": query,
            "api_key": api_key,
            "num": num_results,
            "hl": "th",
            "gl": "th"
        })
        results = search.get_dict()
        organic = results.get("organic_results", [])
        return [r.get("link") for r in organic[:num_results] if "link" in r]
    except Exception as e:
        print(f"❌ Error searching Google: {e}")
        return []

# === main logic ===
def ask_with_cli_and_fallback(prompt, api_key):
    print(f"📨 user: {prompt}")
    answer = ask_llm_raw(prompt)
    print("🧠 LLM ตอบโดยตรง:", repr(answer))

    if not is_llm_uncertain(answer):
        return answer

    print("🌐 fallback: ไม่มั่นใจ → Google")
    urls = search_google(prompt, api_key, num_results=1)
    print("🌐 URLs ที่ได้:", urls)

    if not urls:
        return answer + "\n(ไม่สามารถค้นหาข้อมูลเพิ่มเติมได้ในขณะนี้)"

    page_text = scrape_text(urls[0])
    if not page_text:
        return answer + "\n(ไม่สามารถดึงข้อมูลจากเว็บไซต์ได้)"

    refined_prompt = f"จากข้อมูลนี้ ตอบคำถามต่อไปนี้อย่างสั้นกระชับ:\n\n{page_text[:4000]}\n\nคำถาม: {prompt}"
    final_answer = ask_llm_raw(refined_prompt)
    print("🧠 สรุปจาก LLM:", repr(final_answer))
    return final_answer

if __name__ == "__main__":
    if not os.environ.get("SERPAPI_API_KEY"):
        print("❌ ไม่พบ SERPAPI_API_KEY ใน environment")
        sys.exit(1)

    print("พิมพ์คำถาม หรือ 'exit' เพื่อออก")
    while True:
        user_input = input("prompt> ").strip()
        if user_input.lower() in ["exit", "quit"]:
            break
        result = ask_with_cli_and_fallback(user_input, os.environ.get("SERPAPI_API_KEY"))
        print("✅ คำตอบ:", result)

# === FastAPI Route ===
@app.post("/ask")
def route_ask(req: PromptRequest):
    if not req.api_key:
        return {"error": "ต้องระบุ api_key ของ Google Search API"}
    result = ask_with_cli_and_fallback(req.prompt, req.api_key)
    return {"answer": result}