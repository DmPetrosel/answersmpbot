from db.models.models import *
from db.session import async_session

async def get_user(user_id):
    return await async_session.query(User).get(user_id)

async def get_bot_price(promocode :str):
    return await async_session.query(Promo).get(promocode).price