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
async def add_user(user_data : dict = None, **kwargs):
    data = user_data if user_data else kwargs
    user = await UserDAO.add(data)
    return user

@connection
async def add_promocode(promocode_data : dict = None, **kwargs):
    # data = promocode_data if promocode_data else kwargs
    promocode = await PromoDAO.add(promocode_data, **kwargs)
    return promocode

@connection
async def update_promo(promocode_data : dict = None, **kwargs):
    # data = promocode_data if promocode_data else kwargs
    promocode = await PromoDAO.update_by_id(promocode_data, **kwargs)
    return promocode