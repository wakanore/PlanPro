from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Boolean
from datetime import datetime
from sqlalchemy.orm import sessionmaker, declarative_base

metadata = MetaData()

DB_USER= 'postgres'
DB_PASSWORD='5678'
DB_HOST='127.0.0.1'
DB_PORT='5434'
DB_NAME="PlanPro"

DATABASE_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(DATABASE_URL)



local_session = sessionmaker(autoflush=False,
                             autocommit=False, bind=engine)


db = local_session()

Base = declarative_base()



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


metadata.create_all(engine)
