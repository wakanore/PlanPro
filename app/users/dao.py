from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
from app.database import async_session_maker
from app.models import User


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        #Асинхронно находит и возвращает один экземпляр модели по указанным критериям или None.
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        #Асинхронно находит и возвращает один экземпляр модели по указанным критериям или None.
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        #Асинхронно находит и возвращает все экземпляры модели, удовлетворяющие указанным критериям.
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **values):
        #Асинхронно создает новый экземпляр модели с указанными значениями.
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance

    @classmethod
    async def add_many(cls, instances: list[dict]):
        #Асинхронно создает несколько новых экземпляров модели с указанными значениями.
        async with async_session_maker() as session:
            async with session.begin():
                new_instances = [cls.model(**values) for values in instances]
                session.add_all(new_instances)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instances

    @classmethod
    async def update(cls, filter_by, **values):
        #Асинхронно обновляет экземпляры модели, удовлетворяющие критериям фильтрации, указанным в filter_by,
        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    sqlalchemy_update(cls.model)
                    .where(*[getattr(cls.model, k) == v for k, v in filter_by.items()])
                    .values(**values)
                    .execution_options(synchronize_session="fetch")
                )
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount

    @classmethod
    async def delete(cls, delete_all: bool = False, **filter_by):
        #Асинхронно удаляет экземпляры модели, удовлетворяющие критериям фильтрации, указанным в filter_by.
        if delete_all is False:
            if not filter_by:
                raise ValueError("Необходимо указать хотя бы один параметр для удаления.")

        async with async_session_maker() as session:
            async with session.begin():
                query = sqlalchemy_delete(cls.model).filter_by(**filter_by)
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount


class UsersDAO(BaseDAO):
    model = User


