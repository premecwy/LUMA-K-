from llm_core import ask_llm_raw
from search_core import search_google
from scrape_core import scrape_text

FALLBACK_TRIGGERS = [
    "ฉันไม่สามารถตรวจสอบสภาพอากาศ",
    "ฉันเป็นโปรแกรม AI ที่ไม่มีการเชื่อมต่ออินเทอร์เน็ต",
    "คุณสามารถตรวจสอบสภาพอากาศได้จาก",
    "ไม่มีข้อมูล",
    "ไม่สามารถตอบ"
]

def is_llm_uncertain(text: str) -> bool:
    return any(trigger in text for trigger in FALLBACK_TRIGGERS)

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

