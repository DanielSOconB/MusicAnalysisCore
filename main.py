import os
from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Request
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
    """
    return {"message": "Welcome to the Audio Analysis API"}

@app.post("/analyze/")
async def analyze_audio(
    file: UploadFile = File(...),
    user_id: str = Form(...)
):
    # Set the file size limit to 10MB
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    # Check file size directly from the UploadFile object
    file_size = len(await file.read())
    await file.seek(0)  # Reset the file pointer to the beginning
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File size exceeds the limit of 10MB")

    # Validate file type
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
        # Read the uploaded file into memory
        file_bytes = await file.read()

        # Convert audio to WAV format using pydub
        try:
            logging.info("Attempting to convert audio to WAV format...")
            audio = AudioSegment.from_file(io.BytesIO(file_bytes))
            wav_file = io.BytesIO()
            audio.export(wav_file, format="wav")
            wav_file.seek(0)  # Reset pointer to the start
            logging.info("Audio successfully converted in memory")
        except Exception as e:
            logging.error(f"Audio conversion failed: {e}")
            raise HTTPException(status_code=400, detail="Unable to process the provided audio file")

        # Load the WAV file with librosa
        try:
            y, sr = librosa.load(wav_file, sr=None)

            # Extract features
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
            tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
            melody = librosa.feature.mfcc(y=y, sr=sr)
            spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)

            # Prepare the JSON response
            response = {
                "user_id": user_id,
                "tempo": float(tempo),  # Convert to JSON-serializable type
                "chroma_mean": np.mean(chroma, axis=1).tolist(),  # Convert to list
                "tonnetz_mean": np.mean(tonnetz, axis=1).tolist(),  # Convert to list
                "melody_mfcc_mean": np.mean(melody, axis=1).tolist(),  # Convert to list
                "spectral_centroid_mean": np.mean(spectral_centroid, axis=1).tolist(),  # Convert to list
                "message": "Analysis successful"
            }
            return response
        except Exception as e:
            logging.error(f"Error processing audio with librosa: {e}")
            raise HTTPException(status_code=400, detail="Error extracting audio features")

    except HTTPException:
        raise  # Re-raise HTTPExceptions as they are
    except Exception as e:
        logging.error(f"Unexpected error during processing: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error while processing the audio file")

if __name__ == "__main__":
    # Allow access from other devices on the LAN
    uvicorn.run(app, host="0.0.0.0", port=8000)
