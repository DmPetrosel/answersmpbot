from aiogram import Bot, Dispatcher, types
import asyncio
import configparser
from aiogram.filters import Command
bot_list = []

config = configparser.ConfigParser()
config.read('config.ini')
print(config['bot']['token'])
bot = Bot(token=config['bot']['token'])
dp = Dispatcher(bot=bot)

event_loop = asyncio.get_event_loop()
async def start_bot(dp):
    event_loop.create_task(dp.start_polling())
    
async def bot_init(event_loop, token, chat_id):
    bot = Bot(token)
    dp = Dispatcher(bot=bot)
    bot_info = await bot.get_me()
    bot_name = bot_info.username

    bot_list.append({'bot':bot, 'dp':dp, 'username':bot_name, 'chat_id':chat_id})    
    @dp.message(Command('start'))
    async def process_start_command(message: types.Message):
        await message.reply("Привет!\nНапиши мне что-нибудь!")
    
    await start_bot(dp)
    return len(bot_list)-1