from aiogram import Dispatcher, types
import asyncio
import configparser
from aiogram.filters import Command
from db.get import *
from subbot import *
from aiogram.methods import SetMyCommands
from func.main_commands import *
from aide import *
from middleware import *
from func.wb_feedback import *
from classes.taskmanager import *

tasks = []

config = configparser.ConfigParser()
config.read('config.ini')
print(config['bot']['token'])
bot = MyBot(token=config['bot']['token'])
dp = Dispatcher(bot=bot)

async def set_commands_main(bot: MyBot):
    await bot(SetMyCommands(commands=[types.BotCommand(command='start', description='Начать работу'),
                               types.BotCommand(command='help', description='Поддержка'),
                               types.BotCommand(command='pay', description='Пополнить баланс'),
                               types.BotCommand(command='share', description='Пригласить'),
                               types.BotCommand(command='add', description='Новый бот'),
                               types.BotCommand(command='delb', description='Удалить бот'),
                               types.BotCommand(command='addm', description='Добавить менеджера'),
                               types.BotCommand(command='delm', description='Удалить менеджера')
                               ]))





async def init_when_restart():
    bot_from_db = await get_all_bots()
    for ibot in bot_from_db:
        mn = await get_all_register(bot_username=ibot.bot_username, approve=True)
        managers = None
        if mn:
            managers = [i.chat_id for i in mn]
            logging.info(f"======Bot {ibot.bot_username} managers are {managers}========")
        result = await bot_init(ibot.token, ibot.chat_id, managers)
        try:
            list_n, msgs = result
        except:
            list_n = result
        await asyncio.sleep(10)
        if msgs != None:
            for m in msgs: await m.delete()
async def bot_registration(dp :Dispatcher, nbot: MyBot):
    try:
        dp.message.register(nstart, Command('start'))
        dp.message.register(agen, Command('agen'))
        # dp.message.register(help, Command('help'))
        dp.callback_query.register(sbb_callbacks, lambda c: c.data.startswith('sbb'))
        dp.message.register(mess_answering, StateFilter(FeedState.mess_answering))
        dp.message.outer_middleware(NMiddlewareMessage(nbot))
        dp.callback_query.outer_middleware(NMiddlewareCallback(bot, nbot))

        dp.message.register(new_promo, StateFilter('promo_name_state', 'promo_price_state', 'promo_expire_date_state'))

        dp.callback_query.register(callback_marketer, lambda c: c.data in ('my_promos', 'create_promo'))
        dp.message.register(edit_promo, lambda c: c.text.startswith('/edit_promo'))
        await dp.start_polling(nbot)
    finally:
        print("NBOT CLOSE ========")
async def start_bot(dp: Dispatcher, nbot : MyBot):
    tasks.append(asyncio.create_task((bot_registration(dp, nbot))))
    nbot_username = (await nbot.get_me()).username
    bot_info = await get_one_bot(bot_username=nbot_username)
    wb_feed = WBFeedback(bot_username=nbot_username, bot=nbot)
    tasks.append(asyncio.create_task((wb_feed.run())))
    logging.info('AFTER task')
    # stat_o = WBStat(wb_token=bot_info.wb_token, bot_username=nbot_username)
    # tasks.append(asyncio.create_task((stat_o.run())))
    logging.info('AFTER task STOCKS ')
    await set_subbot_commands(nbot)
    tasks.append(asyncio.create_task((nmain_loop(nbot, main_bot=bot))))
    
    
async def bot_init(token:str, chat_id, managers : list):
    try:
        nbot = MyBot(token)
    except Exception as e:
        logging.error(f'Init bot error {e}')
        return None
    ndp = Dispatcher(bot=nbot)
    bot_info = await nbot.get_me()
    if bot_info == None:
        return None
    bot_name = bot_info.username

    bot_list.append({'bot':nbot, 'dp':ndp, 'bot_username':bot_name, 'chat_id':chat_id, 'managers':managers})    
    n = await get_bot_row(bot_username=bot_name)

    msg = await nbot.send_messages('Бот подключён и обновлён.', managers)
    if not msg:
        msg = None   
    await start_bot(ndp, nbot)

    return int(len(bot_list)-1), msg




