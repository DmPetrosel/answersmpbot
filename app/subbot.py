from aiogram import Dispatcher, types
from aide import MyBot
from configparser import ConfigParser
from aiogram.methods import SetMyCommands
from db.get import *
from db.set import *
from db.update import *
import logging
from keyboard.managers_kb import *
from func.ai import *
bot_list = []

async def set_subbot_commands(bot: MyBot):
    await bot(SetMyCommands(commands=[types.BotCommand(command='start', description='Начать работу'),
                               types.BotCommand(command='help', description='Поддержка')]))


async def get_bot_row(chat_id : int = None, dp : Dispatcher = None, bot_username: str = None, bot: MyBot = None):
    '''This method return int number of row of bot_list : list where bot[i]['chat_id'] == chat_id or bot[i]['dp'] == dp or bot[i][bot_username] == bot_username'''
    for i in range(len(bot_list)):
        if bot_list[i]['chat_id'] == chat_id or bot_list[i]['dp'] == dp or bot_list[i]['bot_username'] == bot_username or bot_list[i]['bot'] == bot:
            return i
    return None

async def nstart(message: types.Message, bot: MyBot):
    n_of_list = await get_bot_row(bot=bot)
    config = ConfigParser()
    config.read('config.ini')
    await bot.send_message(message.from_user.id, f"Привет, {message.from_user.first_name}! Я бот АОтветы. \n\nЗдесь буду присылать сообщения с отзывами, а также генерировать ответ на них. Вы можете включить автоматическую отправку сгенерированных сообщений. \n\nА также можете отвечать на сообщения самостоятельно. Когда вы отвечаете самостоятельно, средства с баланса не списываются.\n\nЕсли какие-то вопросы или что-то случилось, напишите нам в поддержку {config.get('support', 'support')}")
    register = await get_register_by_kwargs(chat_id=int(message.from_user.id))
    logging.info(f"Register: {register}")
    if message.from_user.username == None:
        await bot.send_message(message.from_user.id, "Перед началом работы, пожалуйста, добавьте username. \n\nЭто можно сделать в настройках.")
    elif register == None:
        bot_username = (await bot.get_me()).username
        logging.info("add_register: " + str(bot_username))
        await add_register(chat_id=int(message.from_user.id), username=message.from_user.username, name=message.from_user.first_name, bot_username=bot_username)
    # if register and register.approve == False:
    #     await bot.send_message(message.from_user.id, f'Вас ещё не подтвердили как менеджера.\n\nОбратитесь к владельцу бота.\n\nИз главного бота можно выбрать команду "Добавить менеджера".')

async def help(message: types.Message, bot: MyBot):
    config = ConfigParser()
    config.read('config.ini')

    await bot.send_message(message.from_user.id, f"Если что-то случилось или есть вопросы, \n\nнапишите {config.get('support', 'support')}")

# TODO Make this func 
async def get_messages_with_btn ():
    pass


async def callbacks(callback: types.CallbackQuery, bot: MyBot):
    if callback.data == 'sbb_cancel_call':
        await callback.message.edit_text('Действие отменено.\n\nДля управления воспользуйтесь командами')
    elif callback.data == 'sbb_wbfeedsent_yes':
        pass 
    elif callback.data == 'sbb_wbfeedsent_gen':
        pass 
    elif callback.data == 'sbb_wbfeedsent_oneself':
        pass 

async def nmain_loop(bot: MyBot):
    bot_username = (await bot.get_me()).username
    n = await get_bot_row(bot_username=bot_username)
    bot_info = get_one_bot(bot_username=bot_username)
    while True:
        new_messages = await get_all_wbfeed(bot_username=bot_username, is_new=False)
        for mess in new_messages:
            whole_msg = mess.feed_mess + '\n\n'+ mess.materials_links + '\n\n'+ mess.createDate + '\n\nОценка: ' + mess.valuation
            await generate_answer
            sent_mess_list = await bot.send_messages(whole_msg, *bot_list[n]['managers'], reply_markup=await wbfeedsent_kb())
            await update_wbfeed(mess_ids=[sm.id for sm in sent_mess_list], is_new = False)
