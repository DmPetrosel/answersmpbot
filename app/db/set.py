from db.models.models import *
from db.session import async_session

async def set_user(chat_id, username, first_name, promocode=None, is_admin=False):
    user = User(chat_id=chat_id, username=username, first_name=first_name, promocode=promocode, is_admin=is_admin)
    async_session.add(user)
    await async_session.commit()    
    return user
    