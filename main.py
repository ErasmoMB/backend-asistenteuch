from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.core.ai_service import ai_service

app = FastAPI(
    title="API del Asistente Virtual",
    description="API para interactuar con el asistente virtual",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Mensaje(BaseModel):
    texto: str

@app.get("/")
async def root():
    return {
        "mensaje": "Bienvenido a la API del Asistente Virtual",
        "endpoints": {
            "/chat": "POST - Envía un mensaje al asistente",
            "/health": "GET - Verifica el estado del servidor"
        }
    }

@app.post("/chat")
async def chat(mensaje: Mensaje):
    try:
        respuesta = ai_service.obtener_respuesta(mensaje.texto)
        return {"respuesta": respuesta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "asistente-virtual"} 