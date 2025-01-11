from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, field_validator
from typing import List
import base64
import sqlite3
from datetime import datetime
import numpy as np

app = FastAPI()

# Database setup
def init_db():
    conn = sqlite3.connect('iot_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audio_files (
            id INTEGER PRIMARY KEY,
            session_id TEXT,
            timestamp TEXT,
            file_name TEXT,
            length_seconds REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Pydantic models for request validation
class AudioFile(BaseModel):
    file_name: str
    encoded_audio: str

    @field_validator('encoded_audio')
    def validate_base64(cls, v):
        try:
            base64.b64decode(v)
        except Exception:
            raise ValueError('Invalid Base64-encoded audio data')
        return v

class AudioData(BaseModel):
    session_id: str
    timestamp: str
    audio_files: List[AudioFile]

    @field_validator('timestamp')
    def validate_timestamp(cls, v):
        try:
            datetime.fromisoformat(v)
        except ValueError:
            raise ValueError('Invalid ISO-8601 formatted string')
        return v

# Helper function to calculate audio length
def calculate_audio_length(encoded_audio: str, sample_rate: int = 4000) -> float:
    audio_data = base64.b64decode(encoded_audio)
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    length_seconds = len(audio_array) / sample_rate
    return length_seconds

# API endpoint
@app.post("/process-audio")
async def ingest_audio(data: AudioData):
    conn = sqlite3.connect('iot_data.db')
    cursor = conn.cursor()

    processed_files = []

    for audio_file in data.audio_files:
        try:
            length_seconds = calculate_audio_length(audio_file.encoded_audio)
            cursor.execute('''
                INSERT INTO audio_files (session_id, timestamp, file_name, length_seconds)
                VALUES (?, ?, ?, ?)
            ''', (data.session_id, data.timestamp, audio_file.file_name, length_seconds))

            processed_files.append({
                "file_name": audio_file.file_name,
                "length_seconds": length_seconds
            })
        except Exception as e:
            return {"status": "error", "message": str(e)}

    conn.commit()
    conn.close()

    return {"status": "success", "processed_files": processed_files}

# Error handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return {"status": "error", "message": exc.detail}
