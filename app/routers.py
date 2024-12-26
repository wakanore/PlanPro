from typing import Annotated
from fastapi import  Response
from fastui.components import Page, Table, ModelForm
from fastui.forms import fastui_form
from sqlalchemy.exc import SQLAlchemyError
import asyncpg
from app.database import project, task, async_session_maker, users_projects
from sqlalchemy import delete, update
from app.models import SProjectAdd, STaskAdd, User, SUserAuth, UserResponse,  AddProjectORM, AddTaskORM, TaskAdd, ProjectDeleteDone, TaskDeleteDone, Task, Project, ProjectADD, AddGoodORM, Good, UserLogin, UserRegistr
from fastapi import Depends
from fastapi import APIRouter,  status
from app.users.auth import get_password_hash, create_access_token, authenticate_user, get_current_user
from app.users.dao import UsersDAO
from app.models import SUserRegister
from sqlalchemy.sql import text
from datetime import date
from fastapi import  HTTPException
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent
from pydantic import BaseModel

#список возможных ошибок
UserAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Пользователь уже существует')
IncorrectEmailOrPasswordException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                  detail='Неверная почта или пароль')



tasks = [
    Task(id=1, name='Атака', description='Подмена MAC-адреса', start_date=date(1990, 1, 1), end_date=date(1991, 1, 1), id_project=1, done=True),
    Task(id=2, name='Защита', description='MAC-security', start_date=date(1990, 1, 1), end_date=date(1991, 1, 1), id_project=1, done=True)
]


projes = [
    Project(id=1, name='1 Лабораторная работа по Безопасности ОС', description='MAC-Spoofing', start_date=date(2024, 9, 1), end_date=date(2024, 12, 29), done=True),
    Project(id=2, name='Лабораторная работа по электротехнике', description='Аналоговые схемы', start_date=date(2024, 9, 1), end_date=date(2024, 12, 29), done=False),
    Project(id=3, name='Лабораторная работа по СУБД', description='Функции ранжирования', start_date=date(2024, 9, 1), end_date=date(2024, 12, 29), done=False),
    Project(id=4, name='2 Лабораторная работа по Безопасности ОС', description='MAC-Flooding', start_date=date(2024, 9, 1), end_date=date(2024, 12, 29), done=False),
]





router = APIRouter( tags=['Работа с проектами'])

#добавление проекта
@router.post("/add_project")
async def add_project(projectmodel:Annotated[SProjectAdd, Depends()],):
    async with async_session_maker() as session:
        add_project = AddProjectORM(
            id=projectmodel.id,
            name=projectmodel.name,
            description=projectmodel.description,
            start_date=projectmodel.start_date,
            end_date=projectmodel.end_date,
            done=projectmodel.done
        )
        session.add(add_project)
        await session.commit()
        add_data = AddProjectORM(
            id=projectmodel.id,
            id_user=projectmodel.id_user
        )
        session.add(add_data)
        await session.commit()
        return {"ok": True}


#удаление проекта
@router.delete("/delete_project")
async def delete_project(project_id: int):
    async with async_session_maker() as session:
        data_delete = (
            delete(users_projects)
            .where(project.c.id == project_id)
        )
        result = await session.execute(data_delete)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        project_delete = (
            delete(project)
            .where(project.c.id == project_id)
        )
        result = await session.execute(project_delete)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return result.rowcount


#отметить проект как готовый
@router.put("/update_done_project")
async def update_done_project(project_id: int):
    async with async_session_maker() as session:
        project_done = (
            update(project)
            .values(done=True)
            .where(project.c.id==project_id)
        )
        result = await session.execute(project_done)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return result





@router.get("/select_all_project")
async def get_all_projects():
    async with async_session_maker() as session:
        query = 'SELECT name FROM project'
        result = await session.execute(text(query))
        students = result.scalars().all()
        return students

@router.get("/select_project_data")
async def get_project_data(id:int ):
    conn = await asyncpg.connect(user='postgres', password='5678',
                                 database='PlanPro', host='127.0.0.1', port='5434')
    values = await conn.fetch('''SELECT * FROM project WHERE id= $1''', id)
    await conn.close()
    return values

@router.get("/select_project_all_data")
async def get_project_all_data():
    conn = await asyncpg.connect(user='postgres', password='5678',
                                 database='PlanPro', host='127.0.0.1', port='5434')
    values = await conn.fetch('''SELECT * FROM project''')
    await conn.close()
    return values

@router.get("/select_task_data")
async def get_task_data(id:int ):
    conn = await asyncpg.connect(user='postgres', password='5678',
                                 database='PlanPro', host='127.0.0.1', port='5434')
    values = await conn.fetch('''SELECT * FROM task WHERE id= $1''', id)
    await conn.close()
    return values




@router.get("/select_all_task")
async def get_all_tasks():
    async with async_session_maker() as session:
        query = 'SELECT name FROM task'
        result = await session.execute(text(query))
        students = result.scalars().all()
        return students



#добавить задачу к проекту
@router.post("/add_task")
async def add_task(taskmodel:Annotated[STaskAdd, Depends()],):
    async with async_session_maker() as session:
        add_task = AddTaskORM(
            id=taskmodel.id,
            name=taskmodel.name,
            description=taskmodel.description,
            start_date=taskmodel.start_date,
            end_date=taskmodel.end_date,
            done=taskmodel.done,
            id_project=taskmodel.id_project
        )
        session.add(add_task)
        await session.commit()
        return {"ok": True}


#удалить задачу
@router.delete("/delete_task")
async def delete_task(task_id: int ):
    async with async_session_maker() as session:
        task_delete = (
            delete(task)
            .where(task.c.id == task_id)
        )
        result = await session.execute(task_delete)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return result.rowcount


#отметить задачу как готовую
@router.put("/update_done_task")
async def update_done_task(task_id: int):
    async with async_session_maker() as session:
        task_done = (
            update(task)
            .values(done=True)
            .where(task.c.id==task_id)
        )
        result = await session.execute(task_done)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return result.rowcount


#регистрация пользователя
@router.post("/register/")
async def register_user(user_data: SUserRegister) -> dict:
    user = await UsersDAO.find_one_or_none(phone_number=user_data.phone_number)
    if user:
        raise UserAlreadyExistsException
    user_dict = user_data.dict()
    user_dict['password'] = get_password_hash(user_data.password)
    await UsersDAO.add(**user_dict)
    return {'message': f'Вы успешно зарегистрированы!'}



@router.post("/login/login")
async def auth_user(response: Response, user_data: SUserAuth):
    check = await authenticate_user(phone_number=user_data.phone_number, password=user_data.password)
    if check is None:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'ok': True, 'access_token': access_token, 'refresh_token': None, 'message': 'Авторизация успешна!'}


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}


@router.get("/users/me/", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user



CURRENT_ID = 10


@router.get('/api/main', response_model_exclude_none=True)
def get_goods() -> list[AnyComponent]:
    return [
        Page(
            components=[
                Table(
                    data=projes,
                    columns=[
                        DisplayLookup(field='id'),
                        DisplayLookup(field='name'),
                    ]
                )
            ]
        )
    ]


@router.get('/api/', response_model=FastUI, response_model_exclude_none=True)
def add_good_form() -> AnyComponent:
    return [
        Page(
            # таблица проектов
            components=[
                c.Heading(text='Projects', level=2),
                c.Table(
                    data=projes,
                    columns=[
                        DisplayLookup(field='name', on_click=GoToEvent(url='/user/{id}/'))
                    ],
                ),
                # заголовок
                c.Heading(text='Add Project', level=2),
                # добавление проекта
                c.ModelForm(
                    model=ProjectADD,
                    submit_url='/api/main',
                )
            ]
        )
    ]


@router.post('/api/main', response_model_exclude_none=True)
async def add_good(form: Annotated[ProjectADD, fastui_form(ProjectADD)]) -> SProjectAdd:
    async with async_session_maker() as session:
        global CURRENT_ID
        add_project = AddProjectORM(
            id=CURRENT_ID,
            name=form.name,
            description=form.description,
            start_date=form.start_date,
            end_date=form.end_date,
            done=form.done
        )
        CURRENT_ID += 1
        session.add(add_project)
        await session.commit()


class CreateGood(BaseModel):
    id_project: int
    id_user: int


#описание проекта
@router.get("/api/user/{user_id}/", response_model=FastUI, response_model_exclude_none=True)
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
                c.Details(data=user),
                c.Heading(text="Done", level=4),
                c.ModelForm(
                    model=ProjectDeleteDone,
                    submit_url='Done_Project',
                ),
                c.Heading(text="Delete", level=4),
                c.ModelForm(
                    model=ProjectDeleteDone,
                    submit_url='/api/delete_Project',
                ),
                c.Heading(text='Tasks', level=3),
                #просмотр задач
                c.Table(
                    data=projes,
                    columns=[
                        DisplayLookup(field='name', on_click=GoToEvent(url='/tasks/{id}/')),
                    ],
                ),
                #добавление задачи
                c.Heading(text='Add Task', level=3),
                c.ModelForm(
                    model=TaskAdd,
                    submit_url='/api/add_task',
                ),
                #добавление пользователя
                c.Heading(text='Add User by id', level=3),
                c.ModelForm(
                    model=CreateGood,
                    submit_url='/api/users',
                )
            ]
        ),
    ]

@router.get('/api/users', response_model_exclude_none=True)
def get_goods() -> list[AnyComponent]:
    return [
        Page(
            components=[
                Table(
                    data=tasks,
                    columns=[
                        DisplayLookup(field='id'),
                        DisplayLookup(field='name'),
                    ]
                )
            ]
        )
    ]





@router.post('/api/add_task', response_model_exclude_none=True)
async def add_good(form: Annotated[TaskAdd, fastui_form(TaskAdd)]) -> STaskAdd:
    async with async_session_maker() as session:
        add_task = AddTaskORM(
            id=CURRENT_ID,
            name=form.name,
            description=form.description,
            start_date=form.start_date,
            end_date=form.end_date,
            done=form.done,
            id_project=form.id_project
        )
        session.add(add_task)
        await session.commit()



@router.get('/api/add_task', response_model_exclude_none=True)
def get_goods() -> list[AnyComponent]:
    return [
        Page(
            components=[
                Table(
                    data=tasks,
                    columns=[
                        DisplayLookup(field='id'),
                        DisplayLookup(field='name'),
                    ]
                )
            ]
        )
    ]





@router.post('/api/users', response_model_exclude_none=True)
async def add_good(form: Annotated[CreateGood, fastui_form(CreateGood)]) -> Good:
    async with async_session_maker() as session:
        global CURRENT_ID
        CURRENT_ID += 1
        add_user = AddGoodORM(
            id_project=form.id_project,
            id_user=form.id_user,
        )
        session.add(add_user)
        await session.commit()

#описание задач
@router.get("/api/tasks/{id_project}/", response_model=FastUI, response_model_exclude_none=True)
def user_profile(id_project: int) -> list[AnyComponent]:
    try:
        task = next(u for u in tasks if u.id_project == id_project)
    except StopIteration:
        raise HTTPException(status_code=404, detail="User not found")
    return [
        c.Page(
            components=[
                #таблица задач
                c.Heading(text='Tasks', level=2),
                c.Link(components=[c.Text(text='Back')], on_click=BackEvent()),
                c.Table(
                    data=tasks,
                    columns=[
                        DisplayLookup(field='id', mode=DisplayMode.date),
                        DisplayLookup(field='name', mode=DisplayMode.date),
                        DisplayLookup(field='description', mode=DisplayMode.date),
                        DisplayLookup(field='start_date', mode=DisplayMode.date),
                        DisplayLookup(field='end_date', mode=DisplayMode.date),
                        DisplayLookup(field='done', mode=DisplayMode.date),
                    ],
                ),
                c.Heading(text="Delete", level=4),
                c.ModelForm(
                    model=TaskDeleteDone,
                    submit_url='/api/delete_Task',
                ),
                c.Heading(text="Done", level=4),
                c.ModelForm(
                    model=TaskDeleteDone,
                    submit_url='/api/done_Task',
                ),
            ]
        ),
    ]




@router.get('/api/delete_Project', response_model_exclude_none=True)
def get_goods() -> list[AnyComponent]:
    return [
        Page(
            components=[
                Table(
                    data=tasks,
                    columns=[
                        DisplayLookup(field='id'),
                        DisplayLookup(field='name'),
                    ]
                )
            ]
        )
    ]





@router.post('/api/delete_Project', response_model_exclude_none=True)
async def add_good(form: Annotated[ ProjectDeleteDone, fastui_form( ProjectDeleteDone)]) -> ProjectDeleteDone:
    async with async_session_maker() as session:
        project_delete = (
            delete(project)
            .where(project.c.id == form.id)
        )
        result = await session.execute(project_delete)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return result.rowcount


@router.get('/api/Done_Project', response_model_exclude_none=True)
def get_goods() -> list[AnyComponent]:
    return [
        Page(
            components=[
                Table(
                    data=tasks,
                    columns=[
                        DisplayLookup(field='id'),
                        DisplayLookup(field='name'),
                    ]
                )
            ]
        )
    ]





@router.post('/api/Done_Project', response_model_exclude_none=True)
async def add_good(form: Annotated[ ProjectDeleteDone, fastui_form( ProjectDeleteDone)]) -> ProjectDeleteDone:
    async with async_session_maker() as session:
        project_done = (
            update(project)
            .values(done=True)
            .where(project.c.id == form.id)
        )
        result = await session.execute(project_done)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return result




@router.get('/api/login_bec', response_model_exclude_none=True)
def get_goods() -> list[AnyComponent]:
    return [
        Page(
            components=[
                c.Heading(text='Login', level=2)
            ]
        )
    ]


@router.get('/api/login', response_model=FastUI, response_model_exclude_none=True)
def add_good_form() -> AnyComponent:
    return [
        Page(
            components=[
                c.Heading(text='Login', level=2),
                c.Button(text='Registration', on_click=GoToEvent(url='/registration')),
                ModelForm(model=UserLogin, submit_url='/api/login_bec')
            ]
        )
    ]


@router.post('/api/login_bec', response_model_exclude_none=True)
async def add_good(response: Response, form: Annotated[SUserAuth, fastui_form(SUserAuth)]):
    check = await authenticate_user(phone_number=form.phone_number, password=form.password)
    if check is None:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'ok': True, 'access_token': access_token, 'refresh_token': None, 'message': 'Авторизация успешна!'}



@router.get('/api/register_bec', response_model_exclude_none=True)
def get_goods() -> list[AnyComponent]:
    return [
        Page(
            components=[
                c.Heading(text='Register', level=2)
            ]
        )
    ]


@router.get('/api/register', response_model=FastUI, response_model_exclude_none=True)
def add_good_form() -> AnyComponent:
    return [
        Page(
            components=[
                c.Heading(text='Registration', level=2),
                ModelForm(model=UserRegistr, submit_url='/api/register_bec')
            ]
        )
    ]



@router.post('/api/register_bec', response_model_exclude_none=True)
async def add_good(form: Annotated[SUserRegister, fastui_form(SUserRegister)]):
    user = await UsersDAO.find_one_or_none(phone_number=form.phone_number)
    if user:
        raise UserAlreadyExistsException
    user_dict = form.dict()
    user_dict['password'] = get_password_hash(form.password)
    await UsersDAO.add(**user_dict)
    return {'message': f'Вы успешно зарегистрированы!'}



@router.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    return HTMLResponse(prebuilt_html(title='PlanPro'))


