from datetime import date, datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent
from pydantic import BaseModel, Field

app = FastAPI()


class UserLogin(BaseModel):
    phone_number: str
    password: str

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

tasks = [
    Task(id=1, name='n', description='d', start_date=date(1990, 1, 1), end_date=date(1991, 1, 1), id_project=1, done=False),
    Task(id=1, name='n', description='d', start_date=date(1990, 1, 1), end_date=date(1991, 1, 1), id_project=1, done=False),
]


projes = [
    Project(id=1, name='John', description='descr', start_date=date(1990, 1, 1), end_date=date(1991, 1, 1), done=True),
    Project(id=2, name='Johh', description='descr', start_date=date(1990, 1, 1), end_date=date(1991, 1, 1), done=False),
    Project(id=3, name='Job', description='descr', start_date=date(1990, 1, 1), end_date=date(1991, 1, 1), done=False),
    Project(id=4, name='Jod', description='descr', start_date=date(1990, 1, 1), end_date=date(1991, 1, 1), done=False),
]


# define some users



@app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
def users_table() -> list[AnyComponent]:
    return [
        c.Page(
            components=[
                c.Heading(text='Projects', level=2),
                c.Table(
                    data=projes,
                    columns=[
                        DisplayLookup(field='name', on_click=GoToEvent(url='/user/{id}/')),
                        DisplayLookup(field='done', on_click=GoToEvent(url='/login')),
                    ],
                ),
                c.Heading(text='Add Project', level=2),
                c.ModelForm(
                    model=ProjectADD,
                    submit_url='/api/registration',
                )
            ]
        ),
    ]


@app.get("/api/user/{user_id}/", response_model=FastUI, response_model_exclude_none=True)
def user_profile(user_id: int) -> list[AnyComponent]:
    try:
        user = next(u for u in projes if u.id == user_id)
    except StopIteration:
        raise HTTPException(status_code=404, detail="User not found")
    return [
        c.Page(
            components=[
                c.Heading(text=user.name, level=2),
                c.Link(components=[c.Text(text='Back')], on_click=BackEvent()),
                c.Heading(text='Tasks', level=2),
                c.Details(data=user),
                c.Button(text='Done', on_click=GoToEvent(url='/api/')),
                c.Button(text='Delete', on_click=GoToEvent(url='/api/')),
                c.Table(
                    data=projes,
                    columns=[
                        DisplayLookup(field='name', on_click=GoToEvent(url='/tasks/{id}/')),
                    ],
                ),
                c.Heading(text='Add Task', level=3),
                c.ModelForm(
                    model=TaskAdd,
                    submit_url='/api/registration',
                ),
                c.Heading(text='Add User', level=3),
                c.ModelForm(
                    model=NewUser,
                    submit_url='/api/registration',
                )
            ]
        ),
    ]


@app.get("/api/tasks/{id_project}/", response_model=FastUI, response_model_exclude_none=True)
def user_profile(id_project: int) -> list[AnyComponent]:
    try:
        task = next(u for u in tasks if u.id == id_project)
    except StopIteration:
        raise HTTPException(status_code=404, detail="User not found")
    return [
        c.Page(
            components=[
                c.Heading(text='Tasks', level=2),
                c.Link(components=[c.Text(text='Back')], on_click=BackEvent()),
                c.Table(
                    data=tasks,
                    columns=[
                        DisplayLookup(field='name', mode=DisplayMode.date),
                        DisplayLookup(field='description', mode=DisplayMode.date),
                        DisplayLookup(field='start_date', mode=DisplayMode.date),
                        DisplayLookup(field='end_date', mode=DisplayMode.date),
                        DisplayLookup(field='done', mode=DisplayMode.date),
                    ],
                ),
                c.Button(text='Done', on_click=GoToEvent(url='/api/')),
                c.Button(text='Delete', on_click=GoToEvent(url='/api/')),

            ]
        ),
    ]



@app.get("/api/login", response_model=FastUI, response_model_exclude_none=True)
def get_upload_data_page():
    return [
        c.Page(
            components=[
                c.Heading(text='Login', level=2),
                c.Button(text='Registration', on_click=GoToEvent(url='/registration')),
                c.ModelForm(
                    model=UserLogin,
                    submit_url='/api/',
                ),

            ]
        ),
    ]



@app.get("/api/registration", response_model=FastUI, response_model_exclude_none=True)
def get_upload_data_page():
    return [
        c.Page(
            components=[
                c.Heading(text='Registration', level=2),
                c.ModelForm(
                    model=UserRegistr,
                    submit_url='/api/',
                )
            ]
        ),
    ]

@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    return HTMLResponse(prebuilt_html(title='PlanPro'))
