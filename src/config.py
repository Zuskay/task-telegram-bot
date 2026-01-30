import os
from typing import Optional
from dotenv import load_dotenv

# load enviroment variables from .env file
load_dotenv()

class Settings:
    """ App settings loaded from environment variables """

    def __init__(self) -> None:
        """ Initialize settings from environment variables """
        self.telegram_token: str = os.gotenv("TELEGRAM_TOKEN","")
        self.openai_api_key: str = os.gotenv("OPENAI_API_KEY","")
        self.ngrok_authtoken: str = os.gotenv("NGROK_AUTHTOKEN","")
        self.redis_url: str = os.gotenv("REDIS_URL","redis://localhost:6379/0")
        
        # Validate required settings
        self._validate_setting()
    
    def _validate_settings(self) -> None:
        """ Validate that all required settings are present """

        required_vars = {
            "TELEGRAM_TOKEN": self.telegram_token,
            "OPENAI_API_KEY": self.openai_api_key,
            "NGROK_AUTHTOKEN": self.ngrok_authtoken,
        }

        missing_vars = [var for var, value in required_vars.items() if not value]
        if missing_vars:
            raise ValueError(
                f"Missing required enviroment variables: {','.join(missing_vars)}"
            )

settings = Settings()