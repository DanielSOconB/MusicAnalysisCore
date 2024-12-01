Here’s a comprehensive `README.md` tailored for your **Music Analysis Core** project:

---

# **Music Analysis Core**

**Music Analysis Core** is a powerful audio analysis API built using **FastAPI**. It allows users to upload audio files and retrieve detailed audio feature analysis, including tempo, chroma features, tonnetz, MFCCs, and spectral centroids. Designed for developers, music enthusiasts, and researchers, this tool is perfect for building applications in music technology, audio classification, and more.

## **Features**

- 🛠️ **Audio Analysis**: Extracts advanced features like tempo, chroma mean, tonal centroid features (tonnetz), MFCCs, and spectral centroid.
- 🎵 **Audio Formats**: Supports various formats including `.wav`, `.mp3`, `.ogg`, and `.flac`.
- 🌐 **REST API**: Easy-to-use endpoints for audio feature extraction.
- 🚀 **Fast**: Built with **FastAPI** for high performance and scalability.
- 🖥️ **Cross-Platform**: Dockerized for easy deployment anywhere.
- 🌍 **Language Support**: Documentation available in English and extensible to other languages.

---

## **Getting Started**

### **Prerequisites**

- Python 3.12 or later
- Docker (optional, for containerized deployment)
- FFmpeg (required for audio processing)

### **Installation**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/DanielSOconB/MusicAnalysisCore.git
   cd MusicAnalysisCore
   ```

2. **Set Up the Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Install FFmpeg**
   Follow the instructions [here](https://ffmpeg.org/download.html) to install FFmpeg on your system.

4. **Run the Application**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

5. **Access the API**
   Open your browser or API client (e.g., Postman) and go to:
   ```
   http://localhost:8000
   ```

---

## **API Endpoints**

### **Root**
- **URL**: `/`
- **Method**: `GET`
- **Description**: Check the server status.
- **Response**:
  ```json
  {
      "message": "Welcome to the Audio Analysis API"
  }
  ```

### **Analyze Audio**
- **URL**: `/analyze/`
- **Method**: `POST`
- **Description**: Upload an audio file for analysis.
- **Form Data**:
  - `file` (required): The audio file to analyze (WAV, MP3, etc.).
  - `user_id` (required): A unique identifier for the user.
- **Response**:
  ```json
  {
      "user_id": "test_user",
      "tempo": 143.55,
      "chroma_mean": [0.32, 0.31, ...],
      "tonnetz_mean": [0.08, -0.04, ...],
      "melody_mfcc_mean": [-84.7, 90.6, ...],
      "spectral_centroid_mean": [4408.23],
      "message": "Analysis successful"
  }
  ```

---

## **Development and Testing**

### **Run Unit Tests**
Tests are written using `pytest` and include various scenarios, such as valid/invalid audio files and missing parameters.

1. **Run Tests**
   ```bash
   pytest test_app.py
   ```

2. **Test Coverage**
   Ensure that all endpoints and scenarios are covered.

### **Test Files**
Sample test files are located in the `test_files/` directory.

---

## **Docker Deployment**

1. **Build the Docker Image**
   ```bash
   docker build -t music-analysis-core .
   ```

2. **Run the Docker Container**
   ```bash
   docker run -d -p 8000:8000 music-analysis-core
   ```

3. **Access the Application**
   Visit:
   ```
   http://<container-ip>:8000
   ```

---

## **Documentation**

This project uses **Sphinx** for auto-generated documentation.

### **Generate Documentation**
1. **Install Sphinx**
   ```bash
   pip install sphinx
   sphinx-quickstart
   ```

2. **Build HTML Documentation**
   ```bash
   make html
   ```
   The generated documentation will be available in the `_build/html` directory.

---

## **Project Structure**

```
MusicAnalysisCore/
│
├── main.py              # Core FastAPI application
├── test_app.py          # Unit tests for the API
├── test_files/          # Sample audio files for testing
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker build instructions
├── .gitignore           # Git ignored files
├── README.md            # Project documentation
└── docs/                # Sphinx documentation files
```

---

## **Future Features**

- 🔊 **Audio Playback**: Add support for streaming audio.
- 🧠 **ML Models**: Integrate machine learning models for genre classification.
- 📊 **Dashboard**: Build a web interface to visualize audio features.

---

## **Contributing**

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Acknowledgments**

- [FastAPI](https://fastapi.tiangolo.com/) for the API framework.
- [Librosa](https://librosa.org/) for audio feature extraction.
- [FFmpeg](https://ffmpeg.org/) for audio conversion.

Feel free to reach out or submit an issue for any questions or feedback! 😊

--- 

Let me know if you'd like additional changes! 🚀