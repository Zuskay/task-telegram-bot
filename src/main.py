import os
import asyncio
from loguru import logger as log

from cel.connectors.telegram import TelegramConnector
from cel.gateway.message_gateway import MessageGateway, StreamMode  
from cel.assistants.macaw.macaw_assistant import MacawAssistant  
from cel.prompt.prompt_template import PromptTemplate  
from langchain_openai import ChatOpenAI  
  
from src.config import settings  
from src.assistants.task_assistant import TaskAssistant


class AudioProcessingTelegramConnector(TelegramConnector):
    """TelegramConnector customizado que procesa audio a texto"""
    
    def __init__(self, *args, **kwargs):
        from src.audio.audio_processor import AudioProcessor
        self.audio_processor = AudioProcessor(
            telegram_token=kwargs.get('token'),
            openai_key=settings.openai_api_key
        )
        super().__init__(*args, **kwargs)
    
    async def _TelegramConnector__process_message(self, message: dict):
        """Override para procesar audio antes de enviar al gateway"""
        try:
            # Procesar audio si existe
            if "message" in message and "voice" in message["message"]:
                voice = message["message"]["voice"]
                file_id = voice.get("file_id")
                
                if file_id:
                    log.info(f"Procesando audio: {file_id}")
                    text = await self.audio_processor.audio_to_text(file_id)
                    
                    # Reemplazar voice con text
                    del message["message"]["voice"]
                    message["message"]["text"] = text
                    message["message"]["is_transcribed"] = True
                    
                    log.info(f"Audio transcrito: {text[:50]}...")
        except Exception as e:
            log.error(f"Error procesando audio: {str(e)}")
            message["message"]["text"] = "[Error procesando audio]"
        
        # Llamar al método original del padre
        await super()._TelegramConnector__process_message(message)

def main():  
    """Main function to start the Telegram CRUD Bot."""  
    log.info("Starting Telegram CRUD Bot...")   
      
    try:  
        # Create the task assistant  
        task_assistant = TaskAssistant()  
        assistant = task_assistant.assistant 
          
        # Create the message gateway  
        gateway = MessageGateway(  
            assistant=assistant,  
            host="127.0.0.1",  
            port=5004,  
        )  
          
        # Create and register the Telegram connector with audio processing
        connector = AudioProcessingTelegramConnector(  
            token=settings.telegram_token,  
            stream_mode=StreamMode.SENTENCE
        )  
        gateway.register_connector(connector)  
          
        log.info("Bot configuration completed. Starting gateway...")  
        log.info(f"Telegram bot token: {settings.telegram_token[:10]}...")  
        log.info(f"OpenAI API key: {settings.openai_api_key[:10]}...")  
        log.info(f"Redis URL: {settings.redis_url}")  
        log.info("Audio processing (STT) enabled with Whisper API")
          
        # Start the gateway with ngrok enabled  
        gateway.run(enable_ngrok=True)  
          
    except Exception as e:  
        log.error(f"Error starting bot: {e}")  
        raise  
  
  
if __name__ == "__main__":  
    main()