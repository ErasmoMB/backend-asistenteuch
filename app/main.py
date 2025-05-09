from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import speech_recognition as sr
import pyttsx3
from app.api.routes import chat
from app.core.voice_service import voice_service
from app.core.ai_service import ai_service

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

# Inicializar servicios
engine = pyttsx3.init()
engine.setProperty('voice', 'spanish')
engine.setProperty('rate', 150)

recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Ajustar el reconocedor
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API del Asistente Virtual"}

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ Cliente conectado")
    
    try:
        # Mensaje de bienvenida
        await websocket.send_json({
            "type": "response",
            "text": "Hola, soy tu asistente virtual. ¿En qué puedo ayudarte?"
        })
        
        while True:
            # Recibir audio del cliente
            data = await websocket.receive_text()
            print("📩 Audio recibido del cliente")
            
            try:
                # Convertir audio a texto
                with microphone as source:
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source)
                    texto = recognizer.recognize_google(audio, language="es-ES")
                    print(f"🎤 Texto reconocido: {texto}")
                
                # Enviar texto reconocido al cliente
                await websocket.send_json({
                    "type": "text",
                    "text": texto
                })
                
                if texto.lower() == "salir":
                    await websocket.send_json({
                        "type": "response",
                        "text": "Hasta luego!"
                    })
                    break
                
                # Obtener respuesta de la IA
                respuesta = ai_service.obtener_respuesta(texto)
                print(f"🤖 Respuesta de IA: {respuesta}")
                
                # Enviar respuesta al cliente
                await websocket.send_json({
                    "type": "response",
                    "text": respuesta
                })
                
            except sr.UnknownValueError:
                await websocket.send_json({
                    "type": "error",
                    "text": "No entendí, intenta de nuevo."
                })
            except sr.RequestError:
                await websocket.send_json({
                    "type": "error",
                    "text": "Error con el servicio de reconocimiento de voz."
                })
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "text": f"Error: {str(e)}"
                })
                
    except Exception as e:
        print(f"❌ Error en la conexión: {str(e)}")
    finally:
        await websocket.close()
        print("❌ Cliente desconectado") 