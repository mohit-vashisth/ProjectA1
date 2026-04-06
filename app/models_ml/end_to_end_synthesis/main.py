import torch
from TTS.tts.models.xtts import XttsAudioConfig  # Import the missing class
from TTS.api import TTS

# Allowlist `XttsAudioConfig` to be safely unpickled
torch.serialization.add_safe_globals([XttsAudioConfig])

# Load TTS Model
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(
    "cuda" if torch.cuda.is_available() else "cpu"
)
