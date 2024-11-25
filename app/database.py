from typing import Annotated
from sqlalchemy import MetaData, Table, Integer, String, Column, DateTime, ForeignKey, Boolean, func
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker, mapped_column, DeclarativeBase, declared_attr, Mapped
import sqlalchemy as sqlalchemy_package

metadata = MetaData()

DB_USER= "postgres"
DB_PASSWORD='5678'
DB_HOST='127.0.0.1'
DB_PORT='5434'
DB_NAME="PlanPro"

str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

local_session = sessionmaker(autoflush=False,
                             autocommit=False, bind=engine)


db = local_session()

#Base = declarative_base()

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]



project = Table('project', metadata,
    Column('id', Integer(), primary_key=True),
    Column('name', String(100)),
    Column('description', String(1000)),
    Column('done', Boolean()),
    Column('start_date', DateTime(), default=datetime.now),
    Column('end_date', DateTime())
)


task = Table('task', metadata,
    Column('id', Integer(), primary_key=True),
    Column('name', String(200), nullable=False),
    Column('start_date', DateTime(), default=datetime.now),
    Column('end_date', DateTime()),
    Column('description', String(1000)),
    Column('done', Boolean()),
    Column('id_project', Integer(), ForeignKey('project.id'))
)


users = Table('users', metadata,
    Column('id', Integer(), primary_key=True),
    Column('name', String(100)),
    Column('password', String(1000)),
    Column('phone_number', String(20)),
    Column('description', String(1000))

)


users_projects = Table('users_projects', metadata,
    Column('id_project', ForeignKey('project.id')),
    Column('id_user', ForeignKey('users.id'))
)



