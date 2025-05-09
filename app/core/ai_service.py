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
        
    def get_response(self, text: str) -> str:
        try:
            if not text or not text.strip():
                return "No te he escuchado bien. ¿Podrías repetirlo?"
            
            print("\n" + "="*50)
            print("PROCESANDO PETICIÓN EN IA")
            print("="*50)
            print(f"Texto recibido: '{text}'")
            
            # Crear un prompt más específico
            prompt = f"""Eres un asistente virtual amigable y servicial. 
            Responde a la siguiente pregunta o comentario de manera natural y conversacional: 
            {text}"""
            
            try:
                print("Enviando prompt a Gemini...")
                response = self.model.generate_content(prompt)
                print(f"Respuesta cruda de Gemini: {response}")
                
                if not response or not response.text:
                    print("Gemini no devolvió una respuesta válida")
                    return "Lo siento, no pude generar una respuesta. ¿Podrías reformular tu pregunta?"
                
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