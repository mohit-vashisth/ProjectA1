from TTS.api import TTS

# Load model (this will download automatically first time)
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

# Generate speech
tts.tts_to_file(
    text="Hello Naveen, your local XTTS is alive.",
    speaker_wav="sample.wav",  # your voice sample
    language="en",
    file_path="output.wav"
)