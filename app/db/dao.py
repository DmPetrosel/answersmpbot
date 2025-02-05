from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.models import *

class BaseDAO:
    model = None

    @classmethod
    async def add(cls, *args, session:AsyncSession, **kwargs):
        '''*args can get a dict in first parameter, other args parameters ignored. kwargs parameter work in all case.'''
        if args and args[0]:
            kwargs.update(args[0])
        new_instance = cls.model(**kwargs)
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance
    @classmethod
    async def update_by_id(cls, *args, session:AsyncSession, **kwargs):
        if args:
            kwargs.update(args[0])
        instance = select(cls.model).where(kwargs['id']==cls.model.id)
        result = await session.execute(instance)
        query = result.scalar_one_or_none()
        for key, value in kwargs.items():
            setattr(query, key, value)
        session.add(query)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return instance
    
    @classmethod
    async def update_dict_where_kwarg(cls, *args, session:AsyncSession, **kwargs):
        instance = select(cls.model)
        for key, value in kwargs.items():
            instance.where(value==getattr(cls.model, key))
        result = await session.execute(instance)
        query = result.scalar_one_or_none()
        for key, value in args[0].items():
            setattr(query, key, value)
        session.add(query)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return instance

    @classmethod
    async def get_all(cls, *args, session:AsyncSession, **kwargs):
        query = select(cls.model)
        if(kwargs):
            for key, value in kwargs.items():
                # query.join(User, cls.model.chat_id == User.chat_id)
                query = query.where(getattr(cls.model, key) == value)
        if(args):
            # query.join(User, cls.model.chat_id == User.chat_id)
            query = query.where(args[0] == cls.model.chat_id)
        result = await session.execute(query)
        records = result.scalars().all()
        return records    
    @classmethod
    async def get_by_chat_id(cls, *args, session:AsyncSession, **kwargs):
        query =select(cls.model).where(args[0] == cls.model.chat_id)
        result = await session.execute(query)
        records = result.scalar_one_or_none()
        return records
    @classmethod
    async def get_by_id(cls, *args, session:AsyncSession, **kwargs):
        query =select(cls.model).where(args[0] == cls.model.id)
        result = await session.execute(query)
        records = result.scalar_one_or_none()
        return records
    @classmethod
    async def get_by_kwarg_one(cls, *args, session:AsyncSession, **kwargs):
        query =select(cls.model)
        for key, value in kwargs.items():
            query = query.where(getattr(cls.model, key)== value)
        result = await session.execute(query)
        records = result.scalar_one_or_none()
        return records
    @classmethod
    async def delete_by_id(cls, *args, session:AsyncSession, **kwargs):
        instance = select(cls.model).where(args[0] == cls.model.id)
        result = await session.execute(instance)
        query = result.scalar_one_or_none()
        session.delete(query)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return instance
        
        
class UserDAO(BaseDAO):
    model = User

class PromoDAO(BaseDAO):
    model = Promo

class InfoBotDAO(BaseDAO):
    model = InfoBot