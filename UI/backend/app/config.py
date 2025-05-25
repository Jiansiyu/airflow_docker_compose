from dotenv import load_dotenv
import os
from typing import Optional
from configparser import ConfigParser
from pydantic_settings import BaseSettings

load_dotenv()  # take environment variables from .env


class Settings(BaseSettings):
    DATABASE_URL: Optional[str]  = None
    # set up the airflow environment

    AIRFLOW_URL: Optional[str] = "http://localhost:8080"
    AIRFLOW_WWW_USER_USERNAME: Optional[str] = None
    AIRFLOW_WWW_USER_PASSWORD:Optional[str] = None


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

