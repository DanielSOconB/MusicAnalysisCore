import os
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
import librosa
import numpy as np
import uvicorn
import io
import logging
from pydub import AudioSegment

logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.get("/")
async def root():
    """
    Root endpoint to check server status.

    Returns:
        dict: A dictionary with a welcome message.
    """
    return {"message": "Welcome to the Audio Analysis API"}

@app.post("/analyze/")
async def analyze_audio(
    file: UploadFile = File(...),
    user_id: str = Form(...)
):
    """
    Analyze an uploaded audio file and extract various features.

    Args:
        file (UploadFile): The audio file to analyze. Supported formats include WAV, MP3, FLAC, etc.
        user_id (str): The ID of the user uploading the file.

    Raises:
        HTTPException: If the file size exceeds 10MB, the file type is invalid, or there is an error processing the audio file.

    Returns:
        dict: A dictionary containing extracted audio features and metadata.
    """
    MAX_FILE_SIZE = 10 * 1024 * 1024

    file_size = len(await file.read())
    await file.seek(0)
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File size exceeds the limit of 10MB")

    logging.info(f"Received file with Content-Type: {file.content_type}")
    if file.content_type not in [
        "audio/wav",
        "audio/x-wav",
        "audio/vnd.wave",
        "audio/wave",
        "audio/mpeg",
        "audio/flac",
        "audio/ogg",
        "audio/mp3"
    ]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    try:
        file_bytes = await file.read()

        try:
            logging.info("Attempting to convert audio to WAV format...")
            audio = AudioSegment.from_file(io.BytesIO(file_bytes))
            wav_file = io.BytesIO()
            audio.export(wav_file, format="wav")
            wav_file.seek(0)
            logging.info("Audio successfully converted in memory")
        except Exception as e:
            logging.error(f"Audio conversion failed: {e}")
            raise HTTPException(status_code=400, detail="Unable to process the provided audio file")

        try:
            y, sr = librosa.load(wav_file, sr=None)
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
            tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
            melody = librosa.feature.mfcc(y=y, sr=sr)
            spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)

            return {
                "user_id": user_id,
                "tempo": float(tempo),
                "chroma_mean": np.mean(chroma, axis=1).tolist(),
                "tonnetz_mean": np.mean(tonnetz, axis=1).tolist(),
                "melody_mfcc_mean": np.mean(melody, axis=1).tolist(),
                "spectral_centroid_mean": np.mean(spectral_centroid, axis=1).tolist(),
                "message": "Analysis successful"
            }
        except Exception as e:
            logging.error(f"Error processing audio with librosa: {e}")
            raise HTTPException(status_code=400, detail="Error extracting audio features")

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Unexpected error during processing: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error while processing the audio file")

if __name__ == "__main__":
    """
    Start the FastAPI application.

    The app will run on host 0.0.0.0 and port 8000, allowing external access.
    """
    uvicorn.run(app, host="0.0.0.0", port=8000)
