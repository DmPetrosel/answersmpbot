from aiogram import Bot, Dispatcher, types
import asyncio
import configparser
from aiogram.filters import Command
from db.get import *
bot_list = []

config = configparser.ConfigParser()
config.read('config.ini')
print(config['bot']['token'])
bot = Bot(token=config['bot']['token'])
dp = Dispatcher(bot=bot)

event_loop = asyncio.get_event_loop()

async def init_when_restart():
    bot_list = await get_all_bots()
    for bot in bot_list:
        await bot_init(event_loop, bot['token'], bot['chat_id'])

async def start_bot(dp):
    event_loop.create_task(dp.start_polling())
    
async def bot_init(event_loop, token, chat_id):
    bot = Bot(token)
    dp = Dispatcher(bot=bot)
    bot_info = await bot.get_me()
    bot_name = bot_info.username
    if bot_info == None:
        return None

    bot_list.append({'bot':bot, 'dp':dp, 'bot_username':bot_name, 'chat_id':chat_id})    
    @dp.message(Command('start'))
    async def process_start_command(message: types.Message):
        await message.reply("Привет!\nНапиши мне что-нибудь!")
    
    await start_bot(dp)
    return int(len(bot_list)-1)

async def get_bot_row(chat_id : int = None, dp : Dispatcher = None):
    '''This method return int number of row of bot_list : list where bot[i]['chat_id'] == chat_id or bot[i]['dp'] == dp'''
    for i in range(len(bot_list)):
        if bot_list[i]['chat_id'] == chat_id or bot_list[i]['dp'] == dp:
            return i
    return None
    