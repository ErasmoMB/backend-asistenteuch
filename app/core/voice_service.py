import edge_tts
import os
from dotenv import load_dotenv

load_dotenv()

class VoiceService:
    def __init__(self):
        # Configuración de EdgeTTS
        self.voice = "es-ES-AlvaroNeural"  # Voz natural en español
        self.output_path = "output_tts.mp3"

    async def hablar(self, texto: str, voz: str = None, idioma: str = None) -> str:
        """Convierte texto a voz usando EdgeTTS y guarda el audio en un archivo MP3. Devuelve la ruta del archivo."""
        print(f"Asistente: {texto}")
        voice_to_use = voz if voz else self.voice
        communicate = edge_tts.Communicate(texto, voice_to_use)
        await communicate.save(self.output_path)
        return self.output_path

voice_service = VoiceService()