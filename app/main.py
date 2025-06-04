from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import chat, tts, uch_api, laboratorios_api, produccion_cientifica_api
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Asistente Virtual API")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://frontend-asistenteuch.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(chat.router, prefix="/api")
app.include_router(tts.router, prefix="/api")
app.include_router(uch_api.router, prefix="/api")
app.include_router(laboratorios_api.router, prefix="/api")
app.include_router(produccion_cientifica_api.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API del Asistente Virtual"}