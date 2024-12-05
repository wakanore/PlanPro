from typing import Annotated
<<<<<<< HEAD
from fastapi import  Depends, APIRouter
from app.database import engine, project, task, users
from sqlalchemy import  delete, update
from app.models import SProjectAdd, STaskAdd, SPUTTask, SPUTProject, SUserRegister
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.users.auth import get_db, authenticate_user, create_access_token, get_user, get_current_user
from app.models import Token
from app.models import UserCreate, UserResponse
from app.models import User
from app.users.auth import get_password_hash
from .models import User as UserModel
=======

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
>>>>>>> 06bd7fd2e8abd184b5468c9f06afe30b9d8f26c5


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

<<<<<<< HEAD
@router.post("/register_user/")
async def add_user(user_model:Annotated[SUserRegister, Depends()],):
    project_add = users.insert().values(
        phone_number = user_model.phone_number,
        name=user_model.name,
        password = user_model.password,
        description=user_model.description
    )

    conn = engine.connect()
    conn.execute(project_add)
    conn.commit()
    return {"ok":True}




@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



@router.get("/me", response_model=User)
def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user


=======


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
>>>>>>> 06bd7fd2e8abd184b5468c9f06afe30b9d8f26c5

