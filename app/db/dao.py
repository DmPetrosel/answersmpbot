from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.models import *

class BaseDAO:
    model = None

    @classmethod
    async def add(cls, session:AsyncSession, **kwargs):
        new_instance = cls.model(**kwargs)
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance
    @classmethod
    async def get_all(cls, *args, session:AsyncSession, **kwargs):
        query = select(cls.model)
        if(kwargs):
            for key, value in kwargs.items():
                query = query.where(getattr(cls.model, key) == value)
        if(args):
            query = query.where(args[0] == cls.model.id)
        result = await session.execute(query)
        records = result.scalars().all()
        return records    
    @classmethod
    async def get_by_chat_id(cls, *args, session:AsyncSession, **kwargs):
        query =select(cls.model).where(args[0] == cls.model.chat_id)
        result = await session.execute(query)
        records = result.scalar_one_or_none()
        return records
    
class UserDAO(BaseDAO):
    model = User

class PromoDAO(BaseDAO):
    model = Promo

class InfoBotDAO(BaseDAO):
    model = InfoBot