from aiogram import Bot, Dispatcher, types
import asyncio
import configparser
from aiogram.filters import Command
from db.get import *
bot_list = []
tasks = []

config = configparser.ConfigParser()
config.read('config.ini')
print(config['bot']['token'])
bot = Bot(token=config['bot']['token'])
dp = Dispatcher(bot=bot)


async def nstart(message: types.Message):
    list_n = await get_bot_row(message.chat.id)
    await bot_list[list_n]['bot'].send_message(message.from_user.id, "Ну, что, начнём? ")

async def main_bot():
    await bot.send_message(chat_id=config['bot']['owner_id'],text='Bot started')
    await dp.start_polling(bot, skip_updates=False)

async def init_when_restart():
    bot_from_db = await get_all_bots()
    for ibot in bot_from_db:
        list_n = await bot_init(tasks, ibot.token, ibot.chat_id)
        

async def start_bot(dp: Dispatcher, bot : Bot):
    task = asyncio.create_task(dp.start_polling(bot))
    asyncio.gather(task)
    dp.message.register(nstart, Command('start'))

async def bot_init(tasks, token, chat_id):
    nbot = Bot(token)
    ndp = Dispatcher(bot=nbot)
    bot_info = await nbot.get_me()
    bot_name = bot_info.username
    if bot_info == None:
        return None

    bot_list.append({'bot':nbot, 'dp':ndp, 'bot_username':bot_name, 'chat_id':chat_id})    
    n = await get_bot_row(chat_id)

    await bot_list[n]['bot'].send_message(chat_id, 'Сообщение работает!')
       
    await start_bot(ndp, nbot)

    return int(len(bot_list)-1)

async def get_bot_row(chat_id : int = None, dp : Dispatcher = None):
    '''This method return int number of row of bot_list : list where bot[i]['chat_id'] == chat_id or bot[i]['dp'] == dp'''
    for i in range(len(bot_list)):
        if bot_list[i]['chat_id'] == chat_id or bot_list[i]['dp'] == dp:
            return i
    return None



