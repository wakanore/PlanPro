from datetime import datetime
from enum import Enum
from typing import List, Optional, Annotated

from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
import psycopg2
import os
from contextlib import asynccontextmanager

from enum import Enum
from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationError
from datetime import date, datetime
from typing import Optional
import re


app = FastAPI(title="PlanPro")

connection = psycopg2.connect(
            database="PlanPro",
            user='postgres',
            password='5678',
            host='127.0.0.1',
            port='5434',
        )
cursor = connection.cursor()







postgres_insert_query = """ INSERT INTO Project (ID, Name, Description, Start_date, End_date, done)
                                       VALUES (%s,%s,%s,%s,%s,%s)"""

postgres_insert_task = """ INSERT INTO Task (ID, Name, Description, Start_date, End_date, id_project, done)
                                       VALUES (%s,%s,%s,%s,%s,%s,%s)"""

postgres_insert_user = """ INSERT INTO User_ (ID, Name, Description, Phone_number)
                                       VALUES (%s,%s,%s,%s)"""

class SProjectAdd(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    date_start: Optional[datetime] = None
    date_end: Optional[datetime] = None
    done: Optional[bool] = False

class SPUTProject(BaseModel):
    id: int
    done: Optional[bool] = False


projects = []

@app.post("/add_project")
async def add_project(project:Annotated[SProjectAdd, Depends()],):
    project_add = (project.id, project.name, project.description, project.date_start, project.date_end, project.done)
    cursor.execute(postgres_insert_query, project_add)
    connection.commit()
    projects.append(project)
    return {"ok":True}


@app.delete("/delete_project")
async def delete_project(id):
    postgres_delete_query = f"DELETE FROM Project WHERE id = '{id}'"
    cursor.execute(postgres_delete_query)
    connection.commit()
    return {"ok":True}

@app.put("/update_done_project")
async def update_done_project(project:Annotated[SPUTProject, Depends()],):
    postgres_update_project = f"UPDATE Project SET done = '{project.done}' WHERE id = '{project.id}' "
    cursor.execute(postgres_update_project)
    connection.commit()
    return {"ok": True}


class STaskAdd(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    date_start: Optional[datetime] = None
    date_end: Optional[datetime] = None
    id_project: int
    done: Optional[bool] = False

class SPUTTask(BaseModel):
    id: int
    done: Optional[bool] = False

tasks = []

@app.post("/add_task")
async def add_task(task:Annotated[STaskAdd, Depends()],):
    task_add = (task.id, task.name, task.description, task.date_start, task.date_end, task.id_project, task.done)
    cursor.execute(postgres_insert_task, task_add)
    connection.commit()
    tasks.append(task)
    return {"ok":True}

@app.delete("/delete_task")
async def delete_task(id):
    postgres_delete = f"DELETE FROM Task WHERE id = '{id}'"
    cursor.execute(postgres_delete)
    connection.commit()
    return {"ok":True}

@app.put("/update_done_task")
async def update_done_task(task:Annotated[SPUTTask, Depends()],):
    postgres_update_query = f"UPDATE task SET done = '{task.done}' WHERE id = '{task.id}' "
    cursor.execute(postgres_update_query)
    connection.commit()
    return {"ok": True}

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

users = []



@app.post("/registr_user")
async def registr_user(user:Annotated[SUser, Depends()],):
    user_add = (user.id, user.name, user.description, user.phone_number)
    cursor.execute(postgres_insert_user, user_add)
    connection.commit()
    users.append(user)
    return {"ok":True}

@app.delete("/delete_user")
async def delete_user(id):
    postgres_delete = f"DELETE FROM User_ WHERE id = '{id}'"
    cursor.execute(postgres_delete)
    connection.commit()
    return {"ok":True}

