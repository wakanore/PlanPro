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






postgres_insert_query = """ INSERT INTO Project (ID, Name, Description, Start_date, End_date)
                                       VALUES (%s,%s,%s,%s,%s)"""

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


@app.delete("/delete_project")
async def delete_project(id):
    postgres_delete_query = f"DELETE FROM Project WHERE id = '{id}'"
    cursor.execute(postgres_delete_query)
    connection.commit()
    return {"ok":True}
