FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y git ffmpeg
RUN git clone https://github.com/DanielSOconB/MusicAnalysisCore.git /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
