@echo off
cd /d "%~dp0"
set STUDY_MODE=local
if exist tools\tesseract\tesseract.exe set "TESSERACT_CMD=%~dp0tools\tesseract\tesseract.exe"
if exist tools\ollama\ollama.exe (
  set "OLLAMA_MODELS=%~dp0models\ollama"
  start "Ollama" /b tools\ollama\ollama.exe serve
)
.venv\Scripts\python.exe serve.py
