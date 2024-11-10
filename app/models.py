from typing import Optional
from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
import re


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


class SUser(BaseModel):
    id: int
    name: str = Field(default=..., min_length=1, max_length=50, description="Имя студента, от 1 до 50 символов")
    phone_number:  str = Field(default=..., description="Номер телефона в международном формате, начинающийся с '+'")
    description: Optional[str] = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        if not re.match(r'^\+\d{1,15}$', values):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')
        return values

