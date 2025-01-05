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
    
class UserDAO(BaseDAO):
    model = User

class PromoDAO(BaseDAO):
    model = Promo

class InfoBotDAO(BaseDAO):
    model = InfoBot