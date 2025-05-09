import speech_recognition as sr
import pyttsx3
import os
from dotenv import load_dotenv

load_dotenv()

class VoiceService:
    def __init__(self):
        # Inicializar motor de voz
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('voice', 'spanish')
        
        # Inicializar reconocedor de voz
        self.recognizer = sr.Recognizer()
        
        # Ajustar el reconocedor
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

    def hablar(self, texto: str) -> None:
        """Convierte texto a voz y lo reproduce"""
        print(f"Asistente: {texto}")
        self.engine.say(texto)
        self.engine.runAndWait()

    def escuchar(self) -> str | None:
        """Escucha y convierte voz a texto"""
        with sr.Microphone() as source:
            print("Habla ahora (o di 'salir' para terminar)...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                texto = self.recognizer.recognize_google(audio, language="es-ES")
                print(f"Tú: {texto}")
                return texto.lower()
            except sr.WaitTimeoutError:
                print("No se detectó audio, intentando de nuevo...")
                return None
            except sr.UnknownValueError:
                print("No entendí, intenta de nuevo.")
                return None
            except Exception as e:
                print(f"Error: {str(e)}")
                return None

voice_service = VoiceService() 