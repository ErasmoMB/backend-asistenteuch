from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import chat, tts, uch_api
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Asistente Virtual API")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(chat.router, prefix="/api")
app.include_router(tts.router, prefix="/api")
app.include_router(uch_api.router)

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API del Asistente Virtual"}