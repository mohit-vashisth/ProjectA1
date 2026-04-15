# voice_api.py
from ui.api.client import APIClient

client = APIClient()

# -------------------------------
# 1. Upload Voice Sample
# -------------------------------
def upload_voice_sample(file):
    """
    Upload raw voice sample to backend

    Args:
        file: Uploaded file from Streamlit

    Returns:
        dict: {voice_id, status}
    """

    if file is None:
        return {"error": "No file provided"}

    files = {
        "file": (file.name, file, file.type)
    }

    return client.post("/voice/upload", files=files)


# -------------------------------
# 2. Generate Voice
# -------------------------------
def generate_voice(text: str, voice_id: str):
    """
    Generate cloned voice audio

    Args:
        text (str): text input
        voice_id (str): selected voice

    Returns:
        dict: {audio_url / audio_base64}
    """

    if not text:
        return {"error": "Text is empty"}

    return client.post(
        "/voice/generate",
        json={
            "text": text,
            "voice_id": voice_id
        }
    )


# -------------------------------
# 3. List Voices
# -------------------------------
def list_voices():
    """
    Fetch all saved voices

    Returns:
        list[dict]
    """

    return client.get("/voice/list")


# -------------------------------
# 4. Delete Voice
# -------------------------------
def delete_voice(voice_id: str):
    """
    Delete a voice by ID

    Args:
        voice_id (str)

    Returns:
        dict
    """

    if not voice_id:
        return {"error": "voice_id required"}

    return client.delete(f"/voice/{voice_id}")


# -------------------------------
# 5. Preview Voice
# -------------------------------
def preview_voice(voice_id: str, text: str = "Hello this is a sample"):
    """
    Quick preview generation

    Args:
        voice_id (str)
        text (str)

    Returns:
        dict
    """

    return client.post(
        "/voice/preview",
        json={
            "voice_id": voice_id,
            "text": text
        }
    )