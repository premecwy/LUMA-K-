# tts_core.py
from TTS.api import TTS
import os

# === โหลด Khanomtan TTS model (local) ===
model_dir = os.path.join(os.path.dirname(__file__), "khanomtan-tts-v1.0")
model_path = os.path.join(model_dir, "best_model.pth")
config_path = os.path.join(model_dir, "config.json")
speakers_path = os.path.join(model_dir, "speakers.pth")

tts = TTS(
    model_path=model_path,
    config_path=config_path,
    vocoder_path=None,
    vocoder_config_path=None,
    progress_bar=True
)
tts.synthesizer.tts_model.speaker_manager.load_ids_from_file(speakers_path)

# === patch เพื่อรองรับ length_scale ===
original_tts = tts.synthesizer.tts
def patched_tts(*args, **kwargs):
    if "length_scale" in kwargs:
        tts.synthesizer.tts_model.length_scale = kwargs["length_scale"]
        kwargs.pop("length_scale")
    return original_tts(*args, **kwargs)

tts.synthesizer.tts = patched_tts

# ✅ ฟังก์ชันหลัก สำหรับเรียกจาก FastAPI ภายนอก
def generate_khanomtan_tts(text: str, output_path: str = "thai_tts_output.wav", length_scale: float = 1.0):
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    tts.tts_to_file(
        text=text,
        file_path=output_path,
        speaker="Tsynctwo",
        language="th-th",
        length_scale=length_scale
    )
    return output_path
