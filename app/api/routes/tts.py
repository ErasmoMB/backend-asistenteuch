from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.core.voice_service import voice_service
import asyncio
import os

router = APIRouter()

class TTSRequest(BaseModel):
    text: str
    voice: str | None = None
    lang: str | None = None

@router.post("/tts")
async def tts(request: TTSRequest):
    try:
        if not request.text or not request.text.strip():
            raise HTTPException(status_code=400, detail="Texto vacío")
        # Generar audio con EdgeTTS usando voz e idioma seleccionados
        audio_path = await voice_service.hablar(request.text, voz=request.voice, idioma=request.lang)
        if not os.path.exists(audio_path):
            raise HTTPException(status_code=500, detail="No se generó el audio")
        # Devolver el archivo de audio como respuesta binaria
        return FileResponse(audio_path, media_type="audio/mpeg", filename="tts.mp3")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
