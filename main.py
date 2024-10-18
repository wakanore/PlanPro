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
            database="PlanPro",
            user='postgres',
            password='5678',
            host='127.0.0.1',
            port='5434',
        )
cursor = connection.cursor()






postgres_insert_query = """ INSERT INTO tasks (id, name, description, date_start, date_end)
                                       VALUES (%s,%s,%s)"""

class STaskAdd(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    date_start: Optional[datetime] = None
    date_end: Optional[datetime] = None


tasks = []

@app.post("/add_project")
async def add_project(task:Annotated[STaskAdd, Depends()],):
    project_add = (task.id, task.name, task.description, task.date_start, task.date_end)
    cursor.execute(postgres_insert_query, project_add)
    connection.commit()
    tasks.append(task)
    return {"ok":True}
