FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends tesseract-ocr libgomp1 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY setup-model.py .
RUN python setup-model.py
COPY . .
ENV STUDY_MODE=cloud HTTPS_ONLY=1
EXPOSE 10000
CMD ["python", "serve.py"]
