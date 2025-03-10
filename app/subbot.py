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
from aiogram.fsm.context import FSMContext
from func.states import *
from func.wb_feedback import *
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

async def nstart(message: types.Message, state: FSMContext, bot: MyBot):
    await state.clear()
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

async def help(message: types.Message, state: FSMContext, bot: MyBot):
    await state.clear()
    config = ConfigParser()
    config.read('config.ini')
    await bot.send_message(message.from_user.id, f"Если что-то случилось или есть вопросы, \n\nнапишите {config.get('support', 'support')}")

# TODO Make this func 
async def get_messages_with_btn ():
    pass


async def callbacks(callback: types.CallbackQuery, state: FSMContext, bot: MyBot):
    if callback.data == 'sbb_cancel_call':
        await callback.message.edit_text('Действие отменено.\n\nДля управления воспользуйтесь командами')
    elif callback.data.startswith('sbb_wbfeedsent_yes'):
        answer_id = callback.data.split('_')[-1]
        ans = await get_one_wbfeedanswer(id=answer_id)
        question_id = ans.question_id
        question = await get_one_wbfeed(id=question_id)
        success = await answer_for_feedback(feedback_id=question.feed_id, text=ans.text)
        if success:
            await callback.message.edit_text('Ответ отправлен')
            await update_wbfeed(id=question.id, is_answering=False, feed_ans=ans.text)
        else:
            await bot.send_message(callback.from_user.id, 'Что-то пошло не так. Попробуйте ещё раз.')
        
        mess_ids = [m.id for m in await get_all_wbfeedanswer(question_id=question_id)] if await get_all_wbfeedanswer(question_id=question_id) else mess.mess_ids
        bot.edit_messages_beside("На сообщение уже дан ответ.", callback.id, mess_ids) 
    elif callback.data == 'sbb_wbfeedsent_gen':
        answer_id = callback.data.split('_')[-1]
        question_id = (await get_one_wbfeedanswer(id=answer_id)).question_id
        mess = await get_one_wbfeed(id=question_id)
        whole_msg = mess.feed_mess + '\n\n'+ mess.materials_links + '\n\n'+ mess.createDate + '\n\nОценка: ' + mess.valuation
        bot_username = (await bot.get_me()).username
        bot_info = await get_one_bot(bot_username=bot_username)
        generated = await generate_answer(bot_info, whole_msg)
        added_data = await add_answer_data(chat_id=callback.from_user.id, text=generated, question_id=mess.id)
        msg = await bot.send_message(whole_msg+'\n\n===Ответ может быть:===\n'+generated, reply_markup=await wbfeedsent_kb(answer_id=mess.id))
        update_wbfeedanswer(id=added_data.id, mess_id= msg.id)

        pass 
    elif callback.data == 'sbb_wbfeedsent_oneself':
        answer_id = callback.data.split('_')[-1]
        question_id = (await get_one_wbfeedanswer(id=answer_id)).question_id
        mess = await get_one_wbfeed(id=question_id)
        await update_wbfeed(id=mess.id, is_answering=True, answering_chat_id=callback.from_user.id)
        mess_ids = [m.id for m in await get_all_wbfeedanswer(question_id=question_id)] if await get_all_wbfeedanswer(question_id=question_id) else mess.mess_ids
        await bot.edit_messages_beside("Другой менеджер уже отвечает на сообщение", callback.id, mess_ids)
        await bot.send_message(callback.from_user.id, text='Введите ответ на сообщение.\n\nПодсказка: могут приходить другие сообщения, но бот будет ожидать ответ на этот отзыв, пока вы не ответите или не нажмёте "Отмена" или выберете какую-нибудь команду.')
        await state.set_state(FeedState.mess_answering)
        pass 

async def mess_answering(message: types.Message, state: FSMContext, bot: MyBot):
    question = await get_one_wbfeed(is_answering=True, answering_chat_id=message.from_user.id)
    success = await answer_for_feedback(feedback_id=question.feed_id, text=message.text)
    if success:
        await bot.send_message(message.from_user.id, 'Ответ отправлен')
        await update_wbfeed(id=question.id, is_answering=False, feed_ans=message.text)
        await state.clear()
    else:
        await bot.send_message(message.from_user.id, 'Что-то пошло не так. Попробуйте ещё раз.\n\nВведите сообщение:')
        await state.set_state(FeedState.mess_answering)
        

async def nmain_loop(bot: MyBot):
    bot_username = (await bot.get_me()).username
    n = await get_bot_row(bot_username=bot_username)
    bot_info = await get_one_bot(bot_username=bot_username)
    while True:
        new_messages = await get_all_wbfeed(bot_username=bot_username, is_new=True)
        for mess in new_messages:
            whole_msg = mess.feed_mess + '\n\n'+ mess.materials_links + '\n\n'+ mess.createDate + '\n\nОценка: ' + mess.valuation
            generated = await generate_answer(bot_info, whole_msg)
            for manag in bot_list[n]['managers']:
                added_data = await add_answer_data(chat_id=manag, text=generated, question_id=mess.id)
                msg = await bot.send_message(whole_msg+'\n\n===Ответ может быть:===\n'+generated, reply_markup=await wbfeedsent_kb(answer_id=mess.id))
                await update_wbfeedanswer(id=added_data.id, mess_id= msg.id)

            await update_wbfeed(id=mess.id, is_new = False)
        await asyncio.sleep(60)