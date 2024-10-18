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

postgres_insert_task = """ INSERT INTO Task (ID, Name, Description, Start_date, End_date, id_project)
                                       VALUES (%s,%s,%s,%s,%s,%s)"""

class SProjectAdd(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    date_start: Optional[datetime] = None
    date_end: Optional[datetime] = None


projects = []

@app.post("/add_project")
async def add_project(project:Annotated[SProjectAdd, Depends()],):
    project_add = (project.id, project.name, project.description, project.date_start, project.date_end)
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

class STaskAdd(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    date_start: Optional[datetime] = None
    date_end: Optional[datetime] = None
    id_project: int

tasks = []

@app.post("/add_task")
async def add_task(task:Annotated[STaskAdd, Depends()],):
    task_add = (task.id, task.name, task.description, task.date_start, task.date_end, task.id_project)
    cursor.execute(postgres_insert_task, task_add)
    connection.commit()
    tasks.append(task)
    return {"ok":True}

@app.delete("/delete_task")
async def delete_task(id):
    postgres_delete = f"DELETE FROM Task WHERE id = '{id}'"
    cursor.execute(postgres_delete)
    connection.commit()
    return {"ok":True1}

