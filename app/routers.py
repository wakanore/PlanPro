from typing import Annotated
from fastapi import  Response
from sqlalchemy.exc import SQLAlchemyError
from app.database import project, task, async_session_maker
from sqlalchemy import delete, update
from app.models import SProjectAdd, STaskAdd, User, SUserAuth, UserResponse, AddUserProjectORM, SAddUSer, AddProjectORM, AddTaskORM
from fastapi import Depends
from fastapi import APIRouter, HTTPException, status
from app.users.auth import get_password_hash, create_access_token, authenticate_user, get_current_user
from app.users.dao import UsersDAO
from app.models import SUserRegister

#список возможных ошибок
UserAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Пользователь уже существует')
IncorrectEmailOrPasswordException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                  detail='Неверная почта или пароль')


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
        return {"ok": True}


#удаление проекта
@router.delete("/delete_project")
async def delete_project(project_id: int):
    async with async_session_maker() as session:
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


@router.get("/users/me/", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


#добавить пользователя в проект
@router.post("/add_user_into_project")
async def add_user_into_project(usermodel:Annotated[SAddUSer, Depends()],):
    async with async_session_maker() as session:
        add_user = AddUserProjectORM(id_project=usermodel.id_project, id_user=usermodel.id_user)
        session.add(add_user)
        await session.commit()
        return {"ok": True}

