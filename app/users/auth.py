from email._header_value_parser import get_token
from http.client import HTTPException
from fastapi import Depends
from jose import jwt
from datetime import datetime, timedelta, timezone
import hashlib
from rich import status
from app.config import get_auth_data
from app.users.dao import UsersDAO


#возвращает хешированный пароль
def get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

#проверка верности пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return get_password_hash(plain_password)== hashed_password

#создает и возвращает токен доступа
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt

#аутентификация пользователя
async def authenticate_user(phone_number: str, password: str):
    user = await UsersDAO.find_one_or_none(phone_number=phone_number)
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user


#возвращает текущего пользователя
async def get_current_user(token: str = Depends(get_token)):
    auth_data = get_auth_data()
    payload = jwt.decode(token, auth_data['secret_key'], algorithms=auth_data['algorithm'])
    expire: str = payload.get('exp')
    user_id: str = payload.get('sub')
    user = await UsersDAO.find_one_or_none_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user

