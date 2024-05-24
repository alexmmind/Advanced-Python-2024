from typing import ClassVar
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from dotenv import load_dotenv
import os

from pydantic import SecretStr
from dotenv import load_dotenv
import os

class Settings(BaseSettings):
    load_dotenv()
    bot_token: SecretStr
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    DB_PATH: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.DB_PATH = os.getenv('DB_PATH')

config = Settings(DB_PATH=os.getenv('DB_PATH')) 