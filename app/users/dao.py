from app.database import users
from sqlalchemy import async_session_maker
from sqlalchemy.future import select
from app.models import SUser


class BaseDAO:
    @classmethod
    async def find_all_students(cls):
        async with async_session_maker() as session:
            query = select(users)
            students = await session.execute(query)
            return students.scalars().all()

class UsersDAO(BaseDAO):
    model = SUser

