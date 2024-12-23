from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

#вход
class UserLogin(BaseModel):
    phone_number: str
    password: str

#регистрация
class UserRegistr(BaseModel):
    password: str
    phone_number: str
    name: str
    description: Optional[str] = None


class Project(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    done: Optional[bool] = False

class Task(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    id_project: int
    done: Optional[bool] = False


class ProjectADD(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class NewUser(BaseModel):
    phone_number: str

class TaskAdd(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    id_project: int
