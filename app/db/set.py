from db.models.models import *
from db.session import *
from db.dao import *
# @connection
# async def set_user(chat_id, username, first_name, session, promocode=None, is_admin=False):
#     user = User(chat_id=chat_id, username=username, first_name=first_name, promocode=promocode, is_admin=is_admin)
#     session.add(user)
#     await session.commit()    
#     return user


@connection
async def add_money_stat(*args, session: AsyncSession, **kwargs):
    mn = await MoneyStatDAO.add(*args, session=session, **kwargs)
    return mn
@connection
async def add_answer_data(*args, session: AsyncSession, **kwargs):
    user = await WBFeedAnswerDAO.add(*args, session=session, **kwargs)
    return user

@connection
async def add_wbfeed(*args, session: AsyncSession, **kwargs):
    user = await WBFeedDataDAO.add(*args, session=session, **kwargs)
    return user

@connection
async def add_user(*args, session: AsyncSession, **kwargs):
    user = await UserDAO.add(*args, session=session, **kwargs)
    return user

@connection
async def add_register(*args, session: AsyncSession, **kwargs):
    register = await RegisterDAO.add(*args, session=session, **kwargs)
    return register

@connection
async def add_promocode(*args, session: AsyncSession, **kwargs):
    # data = promocode_data if promocode_data else kwargs
    promocode = await PromoDAO.add(*args, session=session, **kwargs)
    return promocode

@connection
async def add_bot_info(*args, session: AsyncSession, **kwargs):
    bot_info = await InfoBotDAO.add(*args, session=session, **kwargs)
    return bot_info

@connection
async def update_promo(*args, session: AsyncSession, **kwargs):
    # data = promocode_data if promocode_data else kwargs
    promocode = await PromoDAO.update_by_id(*args, session=session, **kwargs)
    return promocode
@connection
async def update_register(*args, session: AsyncSession, **kwargs):
    # data = promocode_data if promocode_data else kwargs
    register = await RegisterDAO.update_by_id(*args, session=session, **kwargs)
    return register
@connection
async def update_register_dict_where_kwarg(*args, session: AsyncSession, **kwargs):
    register = await RegisterDAO.update_dict_where_kwarg(*args, session=session, **kwargs)
    return register

@connection
async def delete_bot(*args, session: AsyncSession, **kwargs):
    bot_info = await InfoBotDAO.delete_by_id(*args, session=session, **kwargs)
    return bot_info
    

