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
async def add_promocode(*args, **kwargs):
    # data = promocode_data if promocode_data else kwargs
    promocode = await PromoDAO.add(*args, **kwargs)
    return promocode

@connection
async def update_promo(*args, **kwargs):
    # data = promocode_data if promocode_data else kwargs
    promocode = await PromoDAO.update_by_id(*args, **kwargs)
    return promocode