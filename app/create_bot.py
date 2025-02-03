from aiogram import Bot, Dispatcher, types
import asyncio
import configparser
from aiogram.filters import Command
from db.get import *
from subbot import *
from aiogram.methods import SetMyCommands

tasks = []

config = configparser.ConfigParser()
config.read('config.ini')
print(config['bot']['token'])
bot = Bot(token=config['bot']['token'])
dp = Dispatcher(bot=bot)

async def set_commands_main(bot: Bot):
    await bot(SetMyCommands(commands=[types.BotCommand(command='start', description='Начать работу'),
                               types.BotCommand(command='help', description='Поддержка'),
                               types.BotCommand(command='add', description='Добавить новый'),
                               types.BotCommand(command='del', description='Удалить бот'),
                               types.BotCommand(command='addm', description='Добавить менеджера'),
                               types.BotCommand(command='delm', description='Удалить менеджера')
                               ]))

async def main_bot():
    await set_commands_main(bot)
    dp.message.register(help, Command('help'))
    await bot.send_message(chat_id=config['bot']['owner_id'],text='Bot started')
    await dp.start_polling(bot, skip_updates=False)

async def init_when_restart():
    bot_from_db = await get_all_bots()
    for ibot in bot_from_db:
        list_n = await bot_init(ibot.token, ibot.chat_id, ibot.managers)
        

async def start_bot(dp: Dispatcher, bot : Bot):
    tasks.append(asyncio.create_task(dp.start_polling(bot)))
    await set_subbot_commands(bot)
    dp.message.register(nstart, Command('start'))
    dp.message.register(help, Command('help'))

async def bot_init(token:str, chat_id, managers : list):
    nbot = Bot(token)
    ndp = Dispatcher(bot=nbot)
    bot_info = await nbot.get_me()
    bot_name = bot_info.username
    if bot_info == None:
        return None

    bot_list.append({'bot':nbot, 'dp':ndp, 'bot_username':bot_name, 'chat_id':chat_id, 'managers':managers})    
    n = await get_bot_row(bot_username=bot_name)

    await bot_list[n]['bot'].send_message(chat_id, 'Сообщение работает!')
       
    await start_bot(ndp, nbot)

    return int(len(bot_list)-1)




