<<<<<<< HEAD
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
#from .utils import verify_password, get_password_hash, create_access_token
from app.models import TokenData
from app.models import User
from app.database import local_session, engine, Base

Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
=======
from email._header_value_parser import get_token
from http.client import HTTPException
from fastapi import Depends
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
import hashlib

from rich import status

from app.config import get_auth_data
from app.users.dao import UsersDAO

#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return get_password_hash(plain_password)== hashed_password
>>>>>>> 06bd7fd2e8abd184b5468c9f06afe30b9d8f26c5

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

<<<<<<< HEAD


=======
async def authenticate_user(phone_number: str, password: str):
    user = await UsersDAO.find_one_or_none(phone_number=phone_number)
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user



async def get_current_user(token: str = Depends(get_token)):

    auth_data = get_auth_data()
    payload = jwt.decode(token, auth_data['secret_key'], algorithms=auth_data['algorithm'])


    expire: str = payload.get('exp')



    user_id: str = payload.get('sub')


    user = await UsersDAO.find_one_or_none_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user



>>>>>>> 06bd7fd2e8abd184b5468c9f06afe30b9d8f26c5
