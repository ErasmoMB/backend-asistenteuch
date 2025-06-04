import os
from dotenv import load_dotenv
import google.generativeai as genai
import traceback

load_dotenv()

class AIService:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("No se encontró la API key de Gemini")
        
        print("\n" + "="*50)
        print("INICIALIZANDO SERVICIO DE IA")
        print("="*50)
        print(f"API Key encontrada: {'Sí' if api_key else 'No'}")
        
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            print("Gemini API configurada correctamente con modelo gemini-1.5-flash")
            print("="*50 + "\n")
        except Exception as e:
            print(f"Error al configurar Gemini: {str(e)}")
            print(traceback.format_exc())
            print("="*50 + "\n")
            raise
        
    def get_response(self, text: str, history: list = None) -> str:
        try:
            if not text or not text.strip():
                return "No te he escuchado bien. ¿Podrías repetirlo?"
            
            print("\n" + "="*50)
            print("PROCESANDO PETICIÓN EN IA")
            print("="*50)
            print(f"Texto recibido: '{text}'")
            if history:
                print(f"Historial recibido: {history}")

            # Detectar si la pregunta requiere citar o buscar en el historial
            referencia_historial = False
            palabras_clave = [
                "primera pregunta", "primera vez que", "qué te pregunté", "qué te dije", "qué te pedí", "anteriormente", "antes", "previo", "conversación pasada", "lo que te dije", "lo que te pregunté", "lo que te pedí", "recuerdas", "recuerda lo que", "puedes citar", "puedes decirme exactamente"
            ]
            texto_minus = text.lower()
            for palabra in palabras_clave:
                if palabra in texto_minus:
                    referencia_historial = True
                    break

            # Construir el prompt con historial (solo previos)
            conversation = ""
            if history and len(history) > 0:
                for msg in history[-10:]:
                    role = "Usuario" if msg.get("role") == "user" else "Asistente"
                    conversation += f"{role}: {msg.get('content').strip()}\n"
                # Agregar solo la pregunta actual al final
                conversation += f"Usuario: {text.strip()}\nAsistente:"
                prompt = (
                    "Eres un asistente virtual amigable y servicial. "
                    "Responde de forma natural y conversacional, recordando el contexto anterior. "
                    "No repitas saludos como '¡Hola!' si ya has saludado antes.\n"
                    f"Historial de la conversación:\n{conversation}"
                )
                if referencia_historial:
                    prompt += ("\nIMPORTANTE: Si la pregunta hace referencia a algo que el usuario dijo, pidió o preguntó antes, revisa el historial y responde citando literalmente la frase o pregunta original del usuario, sin parafrasear ni inventar. Si no encuentras la información, dilo explícitamente.")
            else:
                prompt = (
                    "Eres un asistente virtual amigable y servicial. "
                    "Responde de forma natural y conversacional.\n"
                    f"Usuario: {text.strip()}\nAsistente:"
                )
            
            try:
                print("Enviando prompt a Gemini...")
                response = self.model.generate_content(prompt)
                print(f"Respuesta cruda de Gemini: {response}")
                
                if not response or not response.text:
                    print("Gemini no devolvió una respuesta válida")
                    return "Lo siento, no pude generar una respuesta. ¿Podrías reformular tu pregunta?"
                
                # Filtrar saludos automáticos si ya hay historial
                if history and len(history) > 0:
                    filtered = response.text.lstrip()
                    for saludo in ["¡Hola!", "Hola!", "Hola", "¡Hola"]:
                        if filtered.startswith(saludo):
                            filtered = filtered[len(saludo):].lstrip(' ,.!\n')
                    print(f"Respuesta procesada de Gemini (filtrada): '{filtered}'")
                    print("="*50 + "\n")
                    return filtered
                
                print(f"Respuesta procesada de Gemini: '{response.text}'")
                print("="*50 + "\n")
                return response.text
                
            except Exception as genai_error:
                print(f"Error específico de Gemini: {str(genai_error)}")
                print(traceback.format_exc())
                print("="*50 + "\n")
                raise
            
        except Exception as e:
            print(f"Error general al obtener respuesta de Gemini: {str(e)}")
            print(traceback.format_exc())
            print("="*50 + "\n")
            return "Lo siento, hubo un error al procesar tu pregunta. ¿Podrías intentarlo de nuevo?"

ai_service = AIService()