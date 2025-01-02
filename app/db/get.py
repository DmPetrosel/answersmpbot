from db.models.models import *
from db.session import session

async def get_user(user_id):
    return await session.query(User).get(user_id)

