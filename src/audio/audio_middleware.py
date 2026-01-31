import asyncio
from typing import Any, Dict
from loguru import logger as log


class AudioMiddleware:
    """Middleware que procesa mensajes de audio y los convierte a texto"""
    
    def __init__(self, audio_processor):
        self.audio_processor = audio_processor
    
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa un mensaje y si contiene audio, lo convierte a texto
        
        Args:
            message: Diccionario con datos del mensaje de Telegram
            
        Returns:
            Mensaje modificado con texto transcrito en lugar del audio
        """
        try:
            # Verificar si el mensaje contiene audio
            if "voice" in message and message.get("voice"):
                voice = message["voice"]
                file_id = voice.get("file_id")
                
                if file_id:
                    log.info(f"Procesando audio: {file_id}")
                    
                    # Transcribir audio a texto
                    text = await self.audio_processor.audio_to_text(file_id)
                    
                    # Reemplazar audio con texto transcrito
                    message["text"] = text
                    message["is_transcribed"] = True
                    
                    log.info(f"Audio transcrito: {text[:50]}...")
                    
            elif "audio" in message and message.get("audio"):
                audio = message["audio"]
                file_id = audio.get("file_id")
                
                if file_id:
                    log.info(f"Procesando archivo de audio: {file_id}")
                    
                    # Transcribir audio a texto
                    text = await self.audio_processor.audio_to_text(file_id)
                    
                    # Reemplazar audio con texto transcrito
                    message["text"] = text
                    message["is_transcribed"] = True
                    
                    log.info(f"Audio transcrito: {text[:50]}...")
                    
        except Exception as e:
            log.error(f"Error procesando audio: {str(e)}")
            message["text"] = "[Error procesando audio]"
            
        return message
