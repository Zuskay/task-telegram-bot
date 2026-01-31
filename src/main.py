import os
from loguru import logger as log

from cel.connectors.telegram import TelegramConnector
from cel.gateway.message_gateway import MessageGateway, StreamMode  
from cel.assistants.macaw.macaw_assistant import MacawAssistant  
from cel.prompt.prompt_template import PromptTemplate  
from langchain_openai import ChatOpenAI  
  
from src.config import settings  
from src.assistants.task_assistant import TaskAssistant

def main():  
    """Main function to start the Telegram CRUD bot."""  
    log.info("Starting Telegram CRUD Bot...")  
      
    try:  
        # Create the task assistant  
        task_assistant = TaskAssistant()  
        assistant = task_assistant.get_assistant()  
          
        # Create the message gateway  
        gateway = MessageGateway(  
            assistant=assistant,  
            host="127.0.0.1",  
            port=5004,  
        )  
          
        # Create and register the Telegram connector  
        connector = TelegramConnector(  
            token=settings.telegram_token,  
            stream_mode=StreamMode.SENTENCE  
        )  
        gateway.register_connector(connector)  
          
        log.info("Bot configuration completed. Starting gateway...")  
        log.info(f"Telegram bot token: {settings.telegram_token[:10]}...")  
        log.info(f"OpenAI API key: {settings.openai_api_key[:10]}...")  
        log.info(f"Redis URL: {settings.redis_url}")  
          
        # Start the gateway with ngrok enabled  
        gateway.run(enable_ngrok=True)  
          
    except Exception as e:  
        log.error(f"Error starting bot: {e}")  
        raise  
  
  
if __name__ == "__main__":  
    main()