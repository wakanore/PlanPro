from typing import Annotated

from fastapi import  Response
from app.database import engine, project, task
from sqlalchemy import  delete, update
from app.models import SProjectAdd, STaskAdd, SPUTTask, SPUTProject, User, SUserAuth
from fastapi import Depends
from fastapi import APIRouter, HTTPException, status
from app.users.auth import get_password_hash, create_access_token, authenticate_user, get_current_user
from app.users.dao import UsersDAO
from app.models import SUserRegister
UserAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Пользователь уже существует')
IncorrectEmailOrPasswordException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                  detail='Неверная почта или пароль')


router = APIRouter(prefix='/students', tags=['Работа с проектами'])

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



@router.post("/register/")
async def register_user(user_data: SUserRegister) -> dict:
    user = await UsersDAO.find_one_or_none(phone_number=user_data.phone_number)
    if user:
        raise UserAlreadyExistsException
    user_dict = user_data.dict()
    user_dict['password'] = get_password_hash(user_data.password)
    await UsersDAO.add(**user_dict)
    return {'message': f'Вы успешно зарегистрированы!'}


@router.post("/login/")
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


@router.get("/me/")
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data

