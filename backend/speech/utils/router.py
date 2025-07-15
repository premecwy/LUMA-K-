from fastapi import APIRouter
from pydantic import BaseModel
from speech.stt_core import record_audio, transcribe_audio
from speech.tts_core import generate_khanomtan_tts

router = APIRouter()

class TranscribeRequest(BaseModel):
    filename: str = "thai_input.wav"
    model_size: str = "small"
    device: str = "cpu"
    lang: str = "th"

# --- TTS ---
class TTSRequest(BaseModel):
    text: str
    output_path: str = "thai_tts_output.wav"
    length_scale: float = 1.0

@router.post("/tts")
def tts_api(req: TTSRequest):
    path = generate_khanomtan_tts(req.text, req.output_path, req.length_scale)
    return {"path": path}

# --- STT Record ---
class RecordRequest(BaseModel):
    duration: int = 5
    filename: str = "thai_input.wav"

@router.post("/record")
def route_record(req: RecordRequest):
    filename = record_audio(req.filename, req.duration)
    return {"filename": filename}

# --- STT Transcribe ---
class TranscribeRequest(BaseModel):
    filename: str = "thai_input.wav"
    model_size: str = "small"
    device: str = "cpu"
    lang: str = "th"

@router.post("/transcribe")
def route_transcribe(req: TranscribeRequest):
    text = transcribe_audio(
        filename=req.filename,
        model_size=req.model_size,
        device=req.device,
        lang=req.lang
    )
    return {"transcription": text}