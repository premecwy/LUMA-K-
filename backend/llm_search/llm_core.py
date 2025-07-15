import os
from llama_cpp import Llama

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
