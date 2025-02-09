from db.models.models import *
from db.session import *
from db.dao import *

@connection
async def update_bot_info(*args, **kwargs):
    bot_info = await InfoBotDAO.update_dict_where_kwarg(*args, **kwargs)
    return bot_info

@connection
async def update_register(*args, **kwargs):
    register = await RegisterDAO.update_by_id(*args, **kwargs)
    return register