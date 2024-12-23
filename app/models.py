from typing import Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from sqlalchemy.orm import Mapped
import re
from app.database import Base, str_uniq, int_pk


class SProjectAdd(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    done: Optional[bool] = False

#класс для добавления проекта в бд
class AddProjectORM(Base):
    __tablename__ = "project"
    id: Mapped[int_pk]
    name: Mapped[str]
    description: Mapped[str]
    start_date: Mapped[datetime] = None
    end_date: Mapped[datetime] = None
    done: Mapped[bool] = False

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"


class STaskAdd(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    id_project: int
    done: Optional[bool] = False

#класс для добавления задачи в бд
class AddTaskORM(Base):
    __tablename__ = "task"
    id: Mapped[int_pk]
    name: Mapped[str]
    description: Mapped[str]
    start_date: Mapped[datetime] = None
    end_date: Mapped[datetime] = None
    id_project: Mapped[int]
    done: Mapped[bool] = False

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"


#класс пользователя для работы с бд
class User(Base):
    id: Mapped[int_pk]
    phone_number: Mapped[str]
    name: Mapped[str_uniq]
    description: Mapped[str]
    password: Mapped[str]

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"


#класс с ограничениями для регистрации пользователя
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

#класс аутентификации пользователя
class SUserAuth(BaseModel):
    phone_number: str = Field(..., description="Номер телефона в международном формате, начинающийся с '+'")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")


#модель ответа
class UserResponse(BaseModel):
    username: str
    email: Optional[str] = None


#класс для взаимодействия с бд при добавления пользователя к проекту
class AddUserProjectORM(Base):
    __tablename__ = "users_projects"
    id_project: Mapped[int_pk]
    id_user: Mapped[int_pk]

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

#класс добавления пользователя к проекту
class SAddUSer(BaseModel):
    id_project: int
    id_user: int









