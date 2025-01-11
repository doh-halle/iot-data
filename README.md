FastAPI IoT Data Ingestion Service
Overview

This is a FastAPI backend service, designed to ingest, validate, decode Base64-encoded audio IoT data, and store the metadata in an SQLite database. The API provides an endpoint for uploading audio data and returns a JSON response indicating success or failure.
Features

- Ingest IoT audio data via POST requests

- Validate JSON payload

- Decode audio files and calculate audio length

- Store metadata in an SQLite database

- Return JSON response indicating success or failure


Getting Started

The outlined instructions assume you are working on a debian linux computer and you have installed python3, the python package manager pip and the API testing tool Postman.


Installation 

$git clone https://github.com/doh-halle/iot-data.git
cd iot-data

Install the following dependencies by running the command below on your linux terminal

$ pip install fastapi uvicorn pydantic sqlite3 httpx pytest

Start your API server

$ uvicorn  iotdata:app

Launch your Postman app, at the beginning of the address bar choose the POST method from the dropdown list and and key in the URL - http://127.0.0.1:8000/process-audio into the address bar.

Below the address bar, click the body tab, raw and JSON radio button

In the body of the request, submit any sample data of your choosing which fits the following JSON format:

{
    "session_id": "string",
    "timestamp": "ISO-8601 formatted string",
    "audio_files": [
        {
            "file_name": "string",
            "encoded_audio": "Base64-encoded audio data"
        }
    ]
}

Click the "Send" Button

Response Examples - Upon Success

{
    "status": "success",
    "processed_files": [
        {
            "file_name": "my_sample_audio.mp3",
            "length_seconds": 750.72325
        }
    ]
}

Response Examples - Upon Failure

1 - 
{
    "status": "error",
    "message": "Invalid Base64-encoded audio data"
}

2 - 

{
    "status": "error",
    "message": "Invalid ISO-8601 formatted string"
}

Running Integration Tests

To execute the written tests, run the command below

$ pytest test_iotdata.py

Error Handling

The API includes error handling to ensure that only valid data is processed. If any required fields are missing or if the Base64-encoded audio is invalid, the API will return an error response with a descriptive message.




