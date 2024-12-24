from fastapi import FastAPI
from typing import Annotated
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
from app.models import SAddUSer
from app.routers import router as router_students


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


@app.get('/{path:path}')  # data /api/
def root() -> HTMLResponse:
    return HTMLResponse(prebuilt_html(title='Fastui'))

