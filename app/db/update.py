from db.models.models import *
from db.session import *
from db.dao import *


@connection
async def update_user_by_id(*args, **kwargs):
    user = await UserDAO.update_by_id(*args, **kwargs)
    return user
@connection
async def update_bot_info_dict_by_kw(*args, **kwargs):
    bot_info = await InfoBotDAO.update_dict_where_kwarg(*args, **kwargs)
    return bot_info
@connection
async def update_bot_info_by_id(*args, **kwargs):
    bot_info = await InfoBotDAO.update_by_id(*args, **kwargs)
    return bot_info

@connection
async def update_register(*args, **kwargs):
    register = await RegisterDAO.update_by_id(*args, **kwargs)
    return register

@connection
async def update_wbfeed(*args, **kwargs):
    register = await WBFeedDataDAO.update_by_id(*args, **kwargs)
    return register

@connection
async def update_wbfeedanswer(*args, **kwargs):
    register = await WBFeedAnswerDAO.update_by_id(*args, **kwargs)
    return register
