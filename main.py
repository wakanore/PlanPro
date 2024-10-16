from datetime import datetime
from enum import Enum
from typing import List, Optional, Annotated

from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
import psycopg2
import os
from contextlib import asynccontextmanager


app = FastAPI(title="PlanPro")

connection = psycopg2.connect(
            database="fastapi",
            user='postgres',
            password='password',
            host='127.0.0.1',
            port='5434',
        )
cursor = connection.cursor()



app = FastAPI(title="TO DO LIST")


postgres_insert_query = """ INSERT INTO tasks (id, name, description, date_start, date_end)
                                       VALUES (%s,%s,%s)"""

class STaskAdd(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    date_start: datetime
    date_end: datetime


tasks = []

@app.post("/add_task")
async def add_task(task:Annotated[STaskAdd, Depends()],):
    task_add = (task.id, task.name, task.description, task.date_start, task.date_end)
    cursor.execute(postgres_insert_query, task_add)
    connection.commit()
    tasks.append(task)
    return {"ok":True}