import speech_recognition as sr
import pyttsx3
from app.core.ai_service import ai_service

def main():
    # Inicializar motor de voz
    engine = pyttsx3.init()
    engine.setProperty('voice', 'spanish')
    engine.setProperty('rate', 150)
    
    # Inicializar reconocedor de voz
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    # Ajustar el reconocedor
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8
    
    # Mensaje de bienvenida
    engine.say("Hola, soy tu asistente virtual. ¿En qué puedo ayudarte?")
    engine.runAndWait()
    
    while True:
        with microphone as source:
            print("Habla ahora (o di 'salir' para terminar)...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            
        try:
            texto = recognizer.recognize_google(audio, language="es-ES")
            print(f"Tú: {texto}")
            
            if texto.lower() == "salir":
                engine.say("Hasta luego!")
                engine.runAndWait()
                break
                
            # Obtener respuesta de la IA
            respuesta = ai_service.obtener_respuesta(texto)
            
            # Reproducir respuesta
            print(f"Asistente: {respuesta}")
            engine.say(respuesta)
            engine.runAndWait()
            
        except sr.UnknownValueError:
            print("No entendí, intenta de nuevo.")
        except sr.RequestError:
            print("Error con el servicio de reconocimiento de voz.")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 