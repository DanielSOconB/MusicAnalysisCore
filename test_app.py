import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Define test file paths
VALID_WAV_FILE = "test_files/test_audio.wav"
VALID_MP3_FILE = "test_files/test_audio.mp3"
INVALID_FILE = "test_files/example.txt"
LARGE_AUDIO_FILE = "test_files/large_audio.mp3"
CORRUPTED_AUDIO_FILE = "test_files/corrupted_audio.wav"

# Test the root endpoint
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Audio Analysis API"}

# Test successful analysis with a valid WAV file
def test_analyze_valid_wav():
    with open(VALID_WAV_FILE, "rb") as audio:
        response = client.post(
            "/analyze/",
            files={"file": ("test_audio.wav", audio, "audio/wav")},
            data={"user_id": "test_user"}
        )
    assert response.status_code == 200
    json_data = response.json()
    assert "tempo" in json_data
    assert "chroma_mean" in json_data
    assert "tonnetz_mean" in json_data
    assert "melody_mfcc_mean" in json_data
    assert "spectral_centroid_mean" in json_data
    assert json_data["user_id"] == "test_user"

# Test successful analysis with a valid MP3 file
def test_analyze_valid_mp3():
    with open(VALID_MP3_FILE, "rb") as audio:
        response = client.post(
            "/analyze/",
            files={"file": ("test_audio.mp3", audio, "audio/mpeg")},
            data={"user_id": "test_user"}
        )
    assert response.status_code == 200

# Test missing file
def test_missing_file():
    response = client.post("/analyze/", data={"user_id": "test_user"})
    assert response.status_code == 422

# Test missing user_id
def test_missing_user_id():
    with open(VALID_WAV_FILE, "rb") as audio:
        response = client.post(
            "/analyze/",
            files={"file": ("test_audio.wav", audio, "audio/wav")}
        )
    assert response.status_code == 422

# Test invalid file type
def test_invalid_file_type():
    with open(INVALID_FILE, "rb") as invalid:
        response = client.post(
            "/analyze/",
            files={"file": ("example.txt", invalid, "text/plain")},
            data={"user_id": "test_user"}
        )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid file type"

# Test large file
def test_large_file():
    with open(LARGE_AUDIO_FILE, "rb") as large_file:
        response = client.post(
            "/analyze/",
            files={"file": ("large_audio.mp3", large_file, "audio/mpeg")},
            data={"user_id": "test_user"}
        )
    assert response.status_code == 413
    assert response.json()["detail"] == "File size exceeds the limit of 10MB"

# Test corrupted audio file
def test_corrupted_audio_file():
    with open(CORRUPTED_AUDIO_FILE, "rb") as corrupted:
        response = client.post(
            "/analyze/",
            files={"file": ("corrupted_audio.wav", corrupted, "audio/wav")},
            data={"user_id": "test_user"}
        )
    assert response.status_code == 400
    assert "Unable to process the provided audio file" in response.json()["detail"]
