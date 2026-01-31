import os
import aiohttp
from openai import AsyncOpenAI


class AudioProcessor:
    """Procesa archivos de audio y los convierte a texto usando Whisper API"""
    
    def __init__(self, telegram_token: str, openai_key: str):
        self.telegram_token = telegram_token
        self.openai_client = AsyncOpenAI(api_key=openai_key)
    
    async def download_audio(self, file_id: str) -> bytes:
        """Descarga archivo de audio desde Telegram"""
        try:
            # Obtener información del archivo
            url = f"https://api.telegram.org/bot{self.telegram_token}/getFile"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params={"file_id": file_id}) as resp:
                    data = await resp.json()
                    if not data.get("ok"):
                        raise Exception(f"Error getting file: {data.get('description')}")
                    
                    file_path = data["result"]["file_path"]
                    download_url = f"https://api.telegram.org/file/bot{self.telegram_token}/{file_path}"
                    
                    # Descargar el archivo
                    async with session.get(download_url) as download_resp:
                        return await download_resp.read()
        except Exception as e:
            raise Exception(f"Error descargando audio: {str(e)}")
    
    async def transcribe(self, audio_bytes: bytes, filename: str = "audio.ogg") -> str:
        """Convierte audio a texto usando Whisper API de OpenAI"""
        try:
            # Crear archivo temporal
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as tmp:
                tmp.write(audio_bytes)
                tmp_path = tmp.name
            
            try:
                # Transcribir usando Whisper API
                with open(tmp_path, "rb") as audio_file:
                    transcript = await self.openai_client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        language="es"  # Español por defecto
                    )
                return transcript.text
            finally:
                # Limpiar archivo temporal
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                    
        except Exception as e:
            raise Exception(f"Error transcribiendo audio: {str(e)}")
    
    async def audio_to_text(self, file_id: str) -> str:
        """Descarga y transcribe un archivo de audio en un paso"""
        try:
            audio_bytes = await self.download_audio(file_id)
            text = await self.transcribe(audio_bytes)
            return text
        except Exception as e:
            raise Exception(f"Error procesando audio: {str(e)}")
