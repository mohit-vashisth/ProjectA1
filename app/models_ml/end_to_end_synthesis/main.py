import torch
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from TTS.api import TTS

# -------------------------------
# Device setup (GPU if available)
# -------------------------------
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# -------------------------------
# Load model ONCE (important)
# -------------------------------
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(DEVICE)

# -------------------------------
# FastAPI app
# -------------------------------
app = FastAPI()

# -------------------------------
# Request schema
# -------------------------------
class TTSRequest(BaseModel):
    text: str

# -------------------------------
# API endpoint
# -------------------------------
@app.post("/generate")
def generate_audio(request: TTSRequest):
    output_path = "output.wav"

    # Generate audio
    tts.tts_to_file(
        text=request.text,
        file_path=output_path
    )

    # Return audio file
    return FileResponse(output_path, media_type="audio/wav")