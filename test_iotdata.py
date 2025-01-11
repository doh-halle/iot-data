import pytest
from fastapi.testclient import TestClient
from iotdata import app
import base64
import numpy as np

client = TestClient(app)

def test_audio_ingest():
    # Simulated IoT device audio data
    session_id = "test_session"
    timestamp = "2025-01-11T14:16:00"
    audio_array = np.array([1, 2, 3, 4, 5, 6], dtype=np.int16)  # Placeholder audio data
    encoded_audio = base64.b64encode(audio_array.tobytes()).decode("utf-8")

    # Construct the JSON payload
    payload = {
        "session_id": session_id,
        "timestamp": timestamp,
        "audio_files": [
            {
                "file_name": "test_audio.wav",
                "encoded_audio": encoded_audio
            }
        ]
    }

    # Send a POST request to the /process-audio endpoint
    response = client.post("/process-audio", json=payload)

    # Assert the response status and content
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["processed_files"]) == 1
    assert response.json()["processed_files"][0]["file_name"] == "test_audio.wav"
    assert response