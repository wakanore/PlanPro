from fastapi import FastAPI
from typing import Annotated
from fastapi import  Response
from fastui import AnyComponent, FastUI, prebuilt_html
from fastui.components import Page, Table, ModelForm, Form
from fastui.components.display import DisplayLookup
from fastui.events import BackEvent
from fastui.forms import fastui_form
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse


from datetime import date, datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent
from pydantic import BaseModel, Field
from sqlalchemy.orm import Mapped

from app.database import async_session_maker, Base, int_pk
from app.models import SAddUSer, SUserAuth, SUserRegister
from app.routers import router as router_students, UserLogin, IncorrectEmailOrPasswordException, UserRegistr, \
    UserAlreadyExistsException
from app.users.auth import create_access_token, authenticate_user, get_password_hash
from app.users.dao import UsersDAO

app = FastAPI(title="PlanPro")

app.include_router(router_students)

class Good(BaseModel):
    id: int
    name: str
    price: int


class  CreateGood(BaseModel):
    id_project: int
    id_user: int


class AddGoodORM(Base):
    __tablename__ = "users_projects"
    id_project: Mapped[int_pk]
    id_user: Mapped[int_pk]

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

goods = [
    Good(id=1, name='bread', price=50),
]

class NewUser(BaseModel):
    id: int
    id_project: int




CURRENT_ID = 1


@app.get('/api/goods', response_model_exclude_none=True)
def get_goods() -> list[AnyComponent]:
    return [
        Page(
            components=[
                Table(
                    data=goods,
                    columns=[
                        DisplayLookup(field='id'),
                        DisplayLookup(field='name'),
                    ]
                )
            ]
        )
    ]


@app.get('/api/add-good', response_model=FastUI, response_model_exclude_none=True)
def add_good_form() -> AnyComponent:
    return [
        Page(
            components=[
                ModelForm(model=CreateGood, display_mode='page', submit_url='/api/goods')
            ]
        )
    ]


@app.post('/api/goods', response_model_exclude_none=True)
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






@app.get('/api/login_bec', response_model_exclude_none=True)
def get_goods() -> list[AnyComponent]:
    return [
        Page(
            components=[
                c.Heading(text='Login', level=2)
            ]
        )
    ]


@app.get('/api/login', response_model=FastUI, response_model_exclude_none=True)
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


@app.post('/api/login_bec', response_model_exclude_none=True)
async def add_good(response: Response, form: Annotated[SUserAuth, fastui_form(SUserAuth)]):
    check = await authenticate_user(phone_number=form.phone_number, password=form.password)
    if check is None:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'ok': True, 'access_token': access_token, 'refresh_token': None, 'message': 'Авторизация успешна!'}



@app.get('/api/register_bec', response_model_exclude_none=True)
def get_goods() -> list[AnyComponent]:
    return [
        Page(
            components=[
                c.Heading(text='Register', level=2)
            ]
        )
    ]


@app.get('/api/register', response_model=FastUI, response_model_exclude_none=True)
def add_good_form() -> AnyComponent:
    return [
        Page(
            components=[
                c.Heading(text='Registration', level=2),
                ModelForm(model=UserRegistr, submit_url='/api/register_bec')
            ]
        )
    ]



@app.post('/api/register_bec', response_model_exclude_none=True)
async def add_good(form: Annotated[SUserRegister, fastui_form(SUserRegister)]):
    user = await UsersDAO.find_one_or_none(phone_number=form.phone_number)
    if user:
        raise UserAlreadyExistsException
    user_dict = form.dict()
    user_dict['password'] = get_password_hash(form.password)
    await UsersDAO.add(**user_dict)
    return {'message': f'Вы успешно зарегистрированы!'}


@app.get('/{path:path}')  # data /api/
def root() -> HTMLResponse:
    return HTMLResponse(prebuilt_html(title='Fastui'))



