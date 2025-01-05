from db.models.models import *
from db.session import *
@connection
async def get_user(user_id, session):
    return await session.query(User).get(user_id)
@connection
async def get_bot_price(promocode :str, session):
    return await session.query(Promo).get(promocode).price