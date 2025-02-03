from aiogram import Bot, Dispatcher, types
from configparser import ConfigParser
from aiogram.methods import SetMyCommands
bot_list = []

async def set_subbot_commands(bot: Bot):
    await bot(SetMyCommands(commands=[types.BotCommand(command='start', description='Начать работу'),
                               types.BotCommand(command='help', description='Поддержка')]))


async def get_bot_row(chat_id : int = None, dp : Dispatcher = None, bot_username: str = None, bot: Bot = None):
    '''This method return int number of row of bot_list : list where bot[i]['chat_id'] == chat_id or bot[i]['dp'] == dp or bot[i][bot_username] == bot_username'''
    for i in range(len(bot_list)):
        if bot_list[i]['chat_id'] == chat_id or bot_list[i]['dp'] == dp or bot_list[i]['bot_username'] == bot_username or bot_list[i]['bot'] == bot:
            return i
    return None

async def nstart(message: types.Message, bot: Bot):
    n_of_list = await get_bot_row(bot=bot)
    config = ConfigParser()
    config.read('config.ini')
    await bot.send_message(message.from_user.id, f"Привет, {message.from_user.first_name}! Я бот АОтветы. \n\nЗдесь буду присылать сообщения с отзывами, а также генерировать ответ на них. Вы можете включить автоматическую отправку сгенерированных сообщений. \n\nА также можете отвечать на сообщения самостоятельно. Когда вы отвечаете самостоятельно, средства с баланса не списываются.\n\nЕсли какие-то вопросы или что-то случилось, напишите нам в поддержку {config.get('support', 'support')}")
    if message.from_user.id not in bot_list[n_of_list]['managers']:
        await bot.send_message(message.from_user.id, f'Вас нет в списке менеджеров.\n\nОбратитесь к владельцу бота.\n\nИз главного бота можно выбрать команду "Добавить менеджера".')

async def help(message: types.Message, bot: Bot):
    config = ConfigParser()
    config.read('config.ini')

    await bot.send_message(message.from_user.id, f"Если что-то случилось или есть вопросы, \n\nнапишите {config.get('support', 'support')}")