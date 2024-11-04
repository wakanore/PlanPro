from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric, CheckConstraint, Boolean
from datetime import datetime

metadata = MetaData()

DB_USER= 'postgres'
DB_PASSWORD='5678'
DB_HOST='127.0.0.1'
DB_PORT='5434'
DB_NAME="PlanPro"

DATABASE_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(DATABASE_URL)



Project = Table('Project', metadata,
    Column('id', Integer(), primary_key=True),
    Column('name', String(100)),
    Column('description', String(1000)),
    Column('done', Boolean()),
    Column('start_date', DateTime(), default=datetime.now),
    Column('end_date', DateTime())
)


Task = Table('Task', metadata,
    Column('id', Integer(), primary_key=True),
    Column('name', String(200), nullable=False),
    Column('start_date', DateTime(), default=datetime.now),
    Column('end_date', DateTime()),
    Column('description', String(1000)),
    Column('done', Boolean()),
    Column('id_project', Integer(), ForeignKey('Project.id'))
)


Users = Table('Users', metadata,
    Column('id', Integer(), primary_key=True),
    Column('name', String(100)),
    Column('phone_number', String(20)),
    Column('description', String(1000))

)


Users_projects = Table('Users_projects', metadata,
    Column('id_project', ForeignKey('Project.id')),
    Column('id_user', ForeignKey('Users.id'))
)


metadata.create_all(engine)
