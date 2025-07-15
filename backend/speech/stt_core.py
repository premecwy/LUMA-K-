import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import numpy as np
import tempfile
import os

# 🎙 อัดเสียงจากไมโครโฟน (return: samplerate, audio)
def record_audio(duration=5, samplerate=16000):
    print(f"🎙 เริ่มอัดเสียง {duration} วินาที...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()
    print(f"✅ เสร็จสิ้นการอัดเสียง")
    return samplerate, audio

# 🧠 ถอดเสียงจาก path หรือ array
def transcribe_audio(audio_input, model_size="small", device="cpu", lang="th", samplerate=16000):
    print(f"\n📥 เริ่มถอดเสียงด้วยโมเดล '{model_size}'...")

    model = WhisperModel(model_size, device=device, compute_type="int8")

    # ถ้าเป็น path string
    if isinstance(audio_input, str):
        audio_path = audio_input

    # ถ้าเป็น numpy array → เขียนลง temp file
    elif isinstance(audio_input, np.ndarray):
        temp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        write(temp.name, samplerate, audio_input)
        audio_path = temp.name

    else:
        raise ValueError("audio_input ต้องเป็น path (.wav) หรือ numpy array")

    segments, _ = model.transcribe(audio_path, language=lang)
    full_text = " ".join([seg.text for seg in segments])

    if not isinstance(audio_input, str):
        os.remove(audio_path)

    return full_text.strip()
