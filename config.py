import os
from pydantic import BaseSettings
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Settings(BaseSettings):
    #   check minimum 8 characters, one uppercase letter, one lowercase letter, one number and one special character
    PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

    JWT_ENCODE_KEY: str = os.getenv('JWT_ENCODE_KEY')
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM')

    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
    #   API for verify email with abstractapi.com
    VERIFY_EMAIL_API_KEY: str = os.getenv('VERIFY_EMAIL_API_KEY')


settings = Settings()
