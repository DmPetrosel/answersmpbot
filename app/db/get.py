from db.models.models import *
from db.session import *
from db.dao import *
@connection
async def get_user(chat_id:int, session:AsyncSession, **kwargs):
    return await UserDAO.get_by_chat_id(chat_id, session=session)
@connection
async def get_all_promos(chat_id, session:AsyncSession, **kwargs):
    return await PromoDAO.get_all(chat_id, session=session)

@connection
async def get_promo_by_id(promo_id, session:AsyncSession, **kwargs):
    return await PromoDAO.get_by_id(promo_id, session=session)