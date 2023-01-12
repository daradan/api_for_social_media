import re
import requests
from passlib.context import CryptContext

from config import settings

# declare hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def check_password(password: str) -> bool:
    if re.match(settings.PASSWORD_REGEX, password):
        return True
    return False


def verify_email(email: str) -> bool:
    url = 'https://emailvalidation.abstractapi.com/v1/'
    params = {
        'api_key': settings.VERIFY_EMAIL_API_KEY,
        'email': email,
    }
    response = requests.get(url=url, params=params).json()
    if response['is_disposable_email'].get('value'):
        return False
    return True


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)
