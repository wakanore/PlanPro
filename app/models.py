from typing import Optional
from pydantic import BaseModel, Field, field_validator
<<<<<<< HEAD
from datetime import  datetime
import re

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
=======
from datetime import datetime
from sqlalchemy.orm import Mapped
import re

from app.database import Base, str_uniq, int_pk
>>>>>>> 06bd7fd2e8abd184b5468c9f06afe30b9d8f26c5


class SProjectAdd(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    done: Optional[bool] = False

class SPUTProject(BaseModel):
    id: int
    done: Optional[bool] = False


class STaskAdd(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    id_project: int
    done: Optional[bool] = False

class SPUTTask(BaseModel):
    id: int
    done: Optional[bool] = False


<<<<<<< HEAD
class SUser(BaseModel):
    name: str = Field(default=..., min_length=1, max_length=50, description="Имя студента, от 1 до 50 символов")
    phone_number:  str = Field(default=..., description="Номер телефона в международном формате, начинающийся с '+'")
    description: Optional[str] = None
=======
>>>>>>> 06bd7fd2e8abd184b5468c9f06afe30b9d8f26c5

class User(Base):
    id: Mapped[int_pk]
    phone_number: Mapped[str]
    name: Mapped[str_uniq]
    description: Mapped[str]
    password: Mapped[str]

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

class SUserRegister(BaseModel):
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
    phone_number: str = Field(..., description="Номер телефона в международном формате, начинающийся с '+'")
    name: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    description: Optional[str] = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        if not re.match(r'^\+\d{5,15}$', values):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 5 до 15 цифр')
        return values

class SUserAuth(BaseModel):
    phone_number: str = Field(..., description="Номер телефона в международном формате, начинающийся с '+'")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")








class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None



class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True







