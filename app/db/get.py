from db.models.models import *
from db.session import *
from db.dao import *

@connection
async def get_one_wbfeedanswer_last(*args, session:AsyncSession, **kwargs):
    return await WBFeedAnswerDAO.get_by_kwarg_last_id(*args, session=session, **kwargs)


@connection
async def get_one_wbfeedanswer(*args, session:AsyncSession, **kwargs):
    return await WBFeedAnswerDAO.get_by_kwarg_one(*args, session=session, **kwargs)

@connection
async def get_all_wbfeedanswer(*args, session:AsyncSession, **kwargs):
    return await WBFeedAnswerDAO.get_all(*args, session=session, **kwargs)

@connection
async def get_one_wbfeed(*args, session:AsyncSession, **kwargs):
    return await WBFeedDataDAO.get_by_kwarg_one(*args, session=session, **kwargs)

@connection
async def get_all_wbfeed(*args, session:AsyncSession, **kwargs):
    return await WBFeedDataDAO.get_all(*args, session=session, **kwargs)

@connection
async def get_one_register(*args, session:AsyncSession, **kwargs):
    return await RegisterDAO.get_by_kwarg_one(*args, session=session, **kwargs)

@connection
async def get_user(chat_id:int, session:AsyncSession, **kwargs):
    return await UserDAO.get_by_chat_id(chat_id, session=session)
@connection
async def get_user_by_kwargs(*args, session:AsyncSession, **kwargs):
    return await UserDAO.get_by_kwarg_one(*args, session=session, **kwargs)
@connection
async def get_all_promos(chat_id, session:AsyncSession, **kwargs):
    return await PromoDAO.get_all({'chat_id': chat_id}, session=session)

@connection
async def get_all_bots(*args, session: AsyncSession, **kwargs):
    return await InfoBotDAO.get_all(*args, session=session, **kwargs)

@connection
async def get_one_bot(*args, session: AsyncSession, **kwargs):
    return await InfoBotDAO.get_by_kwarg_one(*args, session=session, **kwargs)

@connection
async def get_promo_by_id(promo_id, session:AsyncSession, **kwargs):
    return await PromoDAO.get_by_id(promo_id, session=session)
@connection
async def get_promo_by_kwargs(*args, session:AsyncSession, **kwargs):
    return await PromoDAO.get_by_kwarg_one(session=session, **kwargs)

@connection
async def get_register_by_kwargs(*args, session:AsyncSession, **kwargs):
    return await RegisterDAO.get_by_kwarg_one(session=session, **kwargs)

@connection
async def get_all_register(*args, session:AsyncSession, **kwargs):
    return await RegisterDAO.get_all(*args, session=session, **kwargs)
