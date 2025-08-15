import os
from llama_cpp import Llama
import json

model_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),  # ✅ อิงจาก llm_core.py
        "llama.cpp", "build", "models", "openthaigpt", "openthaigpt1.5-7B-instruct-Q4KM.gguf"
    )
)
llm = Llama(
    model_path=model_path,
    n_ctx=32768,
    n_threads=8,
    n_batch=512,
    use_mlock=True,
    rope_freq_base=1000000.0,
    chat_format="qwen",
    verbose=False,
    escape=True,
)
 
def ask_llm_raw(prompt: str) -> str:
    output = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": "คุณคือผู้ช่วยตอบคำถามที่ฉลาดและซื่อสัตย์หากไม่มีข้อมูลหรือไม่รู้ให้ตอบว่า 'ไม่รู้'"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.9,
        top_p=0.7,
        top_k=40,
        max_tokens=512,
        repeat_penalty=1.1,
    )
    return output['choices'][0]['message']['content']

import json

def ask_llm_plan_json(text: str) -> dict:
    prompt = f"""
ข้อความ: "{text}"

จงแปลงข้อความนี้ให้อยู่ในรูปแบบ JSON ที่ใช้สำหรับ backend โดยมี intent เป็น "Plan" และ decorated_input ดังนี้:
- goal: เป้าหมายหรือกิจกรรม เช่น "เที่ยวเชียงใหม่"
- location: สถานที่ เช่น "เชียงใหม่"
- duration_days: จำนวนวัน เช่น 5
- detail: รายละเอียดพิเศษ เช่น "งบไม่เกิน 5000, ขอนั่งรถทัวร์" (ถ้าไม่มีให้เว้นเป็น "")

รูปแบบที่ต้องการ:

{{
  "intent": "Plan",
  "decorated_input": {{
    "goal": "...",
    "location": "...",
    "duration_days": ...,
    "detail": "..."
  }}
}}

ห้ามมีคำอธิบายอื่น ห้ามใช้ markdown (` ``` `) ห้ามมีคำว่า 'แน่นอนครับ' ตอบ JSON อย่างเดียว
"""

    response = ask_llm_raw(prompt)

    # 🔧 ล้าง prefix/suffix ที่ model ชอบแถ
    cleaned = (
        response.strip()
        .removeprefix("```json")
        .removeprefix("```")
        .replace("แน่นอนครับ", "")
        .strip()
        .removesuffix("```")
    )

    return json.loads(cleaned)
