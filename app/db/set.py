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
async def add_user(*args, **kwargs):
    user = await UserDAO.add(*args, **kwargs)
    return user

@connection
async def add_register(*args, **kwargs):
    register = await RegisterDAO.add(*args, **kwargs)
    return register

@connection
async def add_promocode(*args, **kwargs):
    # data = promocode_data if promocode_data else kwargs
    promocode = await PromoDAO.add(*args, **kwargs)
    return promocode

@connection
async def add_bot_info(*args, **kwargs):
    bot_info = await InfoBotDAO.add(*args, **kwargs)
    return bot_info

@connection
async def update_promo(*args, **kwargs):
    # data = promocode_data if promocode_data else kwargs
    promocode = await PromoDAO.update_by_id(*args, **kwargs)
    return promocode
@connection
async def update_register(*args, **kwargs):
    # data = promocode_data if promocode_data else kwargs
    register = await RegisterDAO.update_by_id(*args, **kwargs)
    return register
@connection
async def update_register_dict_where_kwarg(*args, **kwargs):
    register = await RegisterDAO.update_dict_where_kwarg(*args, **kwargs)
    return register

@connection
async def delete_bot(*args, **kwargs):
    bot_info = await InfoBotDAO.delete_by_id(*args, **kwargs)
    return bot_info
    