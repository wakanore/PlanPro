from typing import Annotated
from fastapi import FastAPI, Depends, APIRouter
import psycopg2
from app.database import engine, project, task
from sqlalchemy import insert, delete, update


from app.models import SProjectAdd, STaskAdd, SPUTTask, SUser, SPUTProject

router = APIRouter(prefix='/students', tags=['Работа со студентами'])

@router.post("/add_project")
async def add_project(projectmodel:Annotated[SProjectAdd, Depends()],):
    project_add = project.insert().values(
        id=projectmodel.id,
        name=projectmodel.name,
        description=projectmodel.description,
        start_date=projectmodel.start_date,
        end_date=projectmodel.end_date,
        done=projectmodel.done
    )

    conn = engine.connect()
    conn.execute(project_add)
    conn.commit()
    return {"ok":True}

@router.delete("/delete_project")
async def delete_project(id):
    s = delete(project).where(
        project.c.id == id
    )
    conn = engine.connect()
    conn.execute(s)
    conn.commit()

    return {"ok":True}

@router.put("/update_done_project")
async def update_done_project(projectmodel:Annotated[SPUTProject, Depends()],):
    s = update(project).where(
        project.c.id == projectmodel.id
    ).values(
        done=projectmodel.done
    )
    conn = engine.connect()
    conn.execute(s)
    conn.commit()
    return {"ok": True}
@router.post("/add_task")
async def add_task(taskmodel:Annotated[STaskAdd, Depends()],):
    project_add = task.insert().values(
        id=taskmodel.id,
        name=taskmodel.name,
        description=taskmodel.description,
        start_date=taskmodel.start_date,
        end_date=taskmodel.end_date,
        done=taskmodel.done,
        id_project=taskmodel.id_project
    )

    conn = engine.connect()
    conn.execute(project_add)
    conn.commit()


    return {"ok":True}

@router.delete("/delete_task")
async def delete_task(id):
    s = delete(task).where(
        task.c.id == id
    )
    conn = engine.connect()
    conn.execute(s)
    conn.commit()

    return {"ok":True}

@router.put("/update_done_task")
async def update_done_task(taskmodel:Annotated[SPUTTask, Depends()],):
    s = update(task).where(
        task.c.id == taskmodel.id
    ).values(
        done=taskmodel.done
    )
    conn = engine.connect()
    conn.execute(s)
    conn.commit()
    return {"ok": True}