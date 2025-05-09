from fastapi import APIRouter, WebSocket, HTTPException
from pydantic import BaseModel
from app.core.ai_service import ai_service
import json
import traceback

router = APIRouter()

class ChatRequest(BaseModel):
    text: str

@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Conexión WebSocket aceptada")

    try:
        while True:
            # Recibir mensaje
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "text":
                # Obtener respuesta de la IA
                response = ai_service.get_response(message["text"])
                
                # Enviar respuesta
                await websocket.send_json({
                    "type": "response",
                    "text": response
                })
            else:
                await websocket.send_json({
                    "type": "error",
                    "text": "Tipo de mensaje no soportado"
                })
                
    except Exception as e:
        print(f"Error en WebSocket: {str(e)}")
        await websocket.send_json({
            "type": "error",
            "text": f"Error: {str(e)}"
        })
    finally:
        await websocket.close()

@router.get("/test")
async def test():
    """Endpoint de prueba para verificar la configuración"""
    try:
        # Probar la conexión con Gemini
        test_response = ai_service.get_response("Hola, ¿cómo estás?")
        return {
            "status": "ok",
            "message": "Backend funcionando correctamente",
            "test_response": test_response
        }
    except Exception as e:
        print(f"Error en el test: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        print("\n" + "="*50)
        print("NUEVA PETICIÓN RECIBIDA")
        print("="*50)
        print(f"Texto recibido del frontend: '{request.text}'")
        print("="*50)
        
        try:
            print("Consultando a la IA...")
            response = ai_service.get_response(request.text)
            print(f"Respuesta de la IA: '{response}'")
            
            response_data = {"response": response}
            print("Enviando al frontend:", json.dumps(response_data, ensure_ascii=False))
            print("="*50 + "\n")
            
            return response_data
            
        except Exception as ai_error:
            print(f"Error en la IA: {str(ai_error)}")
            print("Traceback completo:")
            print(traceback.format_exc())
            raise HTTPException(
                status_code=500,
                detail=f"Error en la IA: {str(ai_error)}"
            )
            
    except Exception as e:
        print(f"Error general: {str(e)}")
        print("Traceback completo:")
        print(traceback.format_exc())
        print("="*50 + "\n")
        raise HTTPException(status_code=500, detail=str(e)) 