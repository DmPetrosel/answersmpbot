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
from func.ping import *
import traceback
bot_list = []
is_paused = {}

async def set_subbot_commands(bot: MyBot):
    await bot(SetMyCommands(commands=[types.BotCommand(command='start', description='Начать работу'),
                               types.BotCommand(command='help', description='Поддержка'),
                               types.BotCommand(command='agen', description='->Авто/Вручную ->Баланс')]))


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
    await bot.send_message(message.from_user.id, f"Привет, {message.from_user.first_name}! Я бот АОтветы. \n\nЗдесь буду присылать сообщения с отзывами, а также генерировать ответ на них. Вы можете включить автоматическую отправку сгенерированных сообщений. \n\nА также можете отвечать на сообщения самостоятельно. Когда ответ на сообщение не генерируется, средства с баланса не списываются.\nСделать нужный настройки автогенерации вы можете по каоманде /agen .\n\nЕсли какие-то вопросы или что-то случилось, напишите нам в поддержку {config.get('support', 'support')}")
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

async def agen(message: types.Message, state: FSMContext, bot: MyBot):
    try:
        await state.clear()
        is_paused[message.chat.id] = True
        manager = await get_register_by_kwargs(chat_id=int(message.from_user.id))
        if manager.principal_chat_id is None:
            bot_info = await get_one_bot(bot_username=manager.bot_username)
            await update_register(id=manager.id, principal_chat_id=bot_info.chat_id)
            manager = await get_register_by_kwargs(chat_id=int(message.from_user.id))
        temp_state_str = ""
        if manager.automated_type == "auto":
            temp_state_str = "автоматическая"
        elif manager.automated_type == "manual":
            temp_state_str = "ручная"
        else:
            temp_state_str = "полуавтоматическая"
        await bot.send_message(message.from_user.id, f"💵 Сейчас на вашем счету {manager.user.balance} Р\n\nℹ️ Пока вы не ответили на это сообщение, вам не будет приходить что-то ещё.\n\nВыберете способ обработки отзывов или оставьте как есть.", reply_markup=await agen_kb(manager.automated_type))
    except Exception as e:
        print(f"agen: {e}\n\n{traceback.format_exc()}")
        logging.error(f"agen: {e}\n\n{traceback.format_exc()}")
# TODO Make this func 
async def get_messages_with_btn ():
    pass


async def sbb_callbacks(callback: types.CallbackQuery, state: FSMContext, bot: MyBot):
    print("\nsbb_callbacks\n")
    print(callback.data)
    if callback.data == 'sbb_cancel_call':
        await state.clear()
        await callback.message.edit_text('Действие отменено.\n\nДля управления воспользуйтесь командами')
    elif callback.data.startswith('sbb_cancel_answer_call'):
        try:
            question_id = int(callback.data.split('_')[-1])
            await state.clear()
            question = await get_one_wbfeed_last(id=question_id)
            await callback.message.edit_text(f'Действие отменено.\n\nДля управления воспользуйтесь командами. Или можете ответить на сообщение по-другому.\n\n{question.feed_mess}', reply_markup=await wb_ans_manual_kb(question_id))
            mess_ids = [[m.chat_id, m.mess_id] for m in await get_all_wbfeedanswer(question_id=question_id)]
            await bot.edit_messages_beside(f"Другой менеджер отменил ответ на этот отзыв: {question.feed_mess}", callback.message.message_id, mess_ids, reply_markup=await wb_ans_manual_kb(question_id))
            is_paused[callback.message.chat.id]= False
        except Exception as e:
            print(f"subbot:sbb_cancel_answer_call: {e}\n\n{traceback.format_exc()}")
            logging.error(f"subbot:sbb_cancel_answer_call: {e}\n\n{traceback.format_exc()}")
    elif callback.data.startswith('sbb_wbfeedsent_yes'):
        print(f"\{callback.data}\n============")
        try:
            answer_id = int(callback.data.split('_')[-1])
            ans = await get_one_wbfeedanswer(id=answer_id)
            question_id = ans.question_id
            question = await get_one_wbfeed_last(id=question_id)
            bot_info = await get_one_bot(bot_username=(await bot.get_me()).username)
            success = await answer_for_feedback(wb_token=bot_info.wb_token, feedback_id=question.feed_id, text=ans.text)
            if success:
                await callback.message.edit_text(f'✅ Ответ отправлен\n\n{question.feed_mess}\n\n✉️ {ans.text}')
                await update_wbfeed(id=question.id, is_answering=False, feed_ans=ans.text)
                mess_ids = []
                mess_ids = [[m.chat_id, m.mess_id] for m in await get_all_wbfeedanswer(question_id=question_id)]
                print("MESS_IDS\n\n"+str(mess_ids)+"\n\n")
        
                await bot.edit_messages_beside(f"✔️ На это сообщение уже дан ответ:\n\n{question.feed_mess}\n\n✉️ {ans.text}", callback.message.message_id, mess_ids) 
       
            else:
                await bot.send_message(callback.from_user.id, f'Что-то пошло не так. На сообщение: \n{question.feed_mess}\n\n Ответить не получилось. Попробуйте ещё раз.\n\n🚀Ответ:\n{ans.text}', await wbfeedsent_kb(answer_id=answer_id))
            
            # mess_ids = ([m.mess_id for m in await get_all_wbfeedanswer(question_id=question_id)] if (len(await get_all_wbfeedanswer(question_id=question_id)) > 0) else mess.mess_ids)
        except Exception as e:
            print(f"subbot:sbb_wbfeedsend_yes: {e}\n\n{traceback.format_exc()}")
            logging.error(f"subbot:sbb_wbfeedsend_yes: {e}\n\n{traceback.format_exc()}")
    elif callback.data.startswith('sbb_wbfeedsent_gen'):
        print(f"\n{callback.data}\n============")
        try:
            if callback.data.split('_')[-2] == 'manual':
                question_id = int(callback.data.split('_')[-1])
            else:
                answer_id = int(callback.data.split('_')[-1])
                question_id = (await get_one_wbfeedanswer(id=answer_id)).question_id
            mess = await get_one_wbfeed_last(id=question_id)
            whole_msg = (str(mess.feed_mess) + '\n\n' if str(mess.feed_mess) else "")+ (str(mess.materials_links) + '\n\n' if str(mess.materials_links) else "") + str(mess.createdDate) + '\n\nОценка: ' + str(mess.valuation)
            bot_username = (await bot.get_me()).username
            bot_info = await get_one_bot(bot_username=bot_username)
            if bot_info.user.balance<=0:
                await bot.send_message(callback.from_user.id, f"❗️❗️❗️На вашем балансе нет средств.\n\nСвяжитесь с администратором бота (@{bot_info.user.username}), чтобы пополнить баланс.")
            generated, total_tokens  = await generate_answer(whole_msg, bot_info, mess.customer_name)
            ex_message = await get_one_wbfeedanswer_last(chat_id=int(callback.from_user.id), question_id=mess.id)
            try:
                added_data = await update_wbfeedanswer(id=ex_message.id, text=generated, total_tokens=ex_message.total_tokens+total_tokens)
                print(f"\nupdate last {added_data}\n")
            except AttributeError:
                added_data = await add_answer_data(question_id=mess.id, chat_id=int(callback.from_user.id), text=generated)
                print(f"\nadd new{added_data}\n")
            except Exception as e:
                print(f"subbot:sbb_wbfeedsend_gen: {e}\n\n{traceback.format_exc()}")
                logging.error(f"subbot:sbb_wbfeedsend_gen: {e}\n\n{traceback.format_exc()}")
            msg = await callback.message.edit_text( text=whole_msg+'\n\n✨ Ответ может быть: ✨\n'+generated, reply_markup=await wbfeedsent_kb(answer_id=added_data.id))
            await update_wbfeedanswer(id=added_data.id, mess_id= msg.message_id)
        except Exception as e:
            print(f"subbot:sbb_wbfeedsend_gen: {e}\n\n{traceback.format_exc()}")
            logging.error(f"subbot:sbb_wbfeedsend_gen: {e}\n\n{traceback.format_exc()}")
        pass 
    elif callback.data.startswith('sbb_wbfeedsent_oneself'):
        print(f"\n{callback.data}\n============")
        if callback.data.split('_')[-2] == 'manual':
                question_id = int(callback.data.split('_')[-1])
        else:    
            answer_id = int(callback.data.split('_')[-1])
            question_id = (await get_one_wbfeedanswer(id=answer_id)).question_id
        await state.set_data(question_id=question_id)
        mess = await get_one_wbfeed_last(id=question_id)
        await update_wbfeed(id=mess.id, is_answering=True, answering_chat_id=callback.from_user.id)
        mess_ids = [[m.chat_id, m.mess_id] for m in await get_all_wbfeedanswer(question_id=question_id)]
        await bot.edit_messages_beside(f"✔️ Другой менеджер уже отвечает на это сообщение:\n\n{mess.feed_mess}", callback.message.message_id, mess_ids)
        temp_answer = await get_one_wbfeedanswer_last(chat_id=int(callback.from_user.id), mess_id=callback.message.message_id)
        await callback.message.delete()
        request_mess = await bot.send_message(callback.from_user.id, text=f'✍️ Введите ответ на это сообщение.\n\n📄 {mess.feed_mess}', reply_markup=await cancel_answer_sbb_kb(question_id=question_id))
        is_paused[callback.message.chat.id] = True
        await update_wbfeedanswer(id=temp_answer.id, mess_id=request_mess.message_id)
        await state.set_state(FeedState.mess_answering)
    elif callback.data.startswith('sbb_handle_'):
        print("=================================RRRRRRRRRRRRRRRRRRRRRRRRRr\n\n\n")
        try:
            agen_type = callback.data.split('_')[-1]
            prefix = ""
            if callback.data.split('_')[-2] == 'current':
                prefix = "Оставили как было: "
            else: 
                prefix = "Обработка сообщений изменена: "
                reg_id = (await get_register_by_kwargs(chat_id=int(callback.from_user.id))).id
                await update_register(id=reg_id, automated_type=agen_type)
            bot_username = (await bot.get_me()).username
            bot_info = await get_one_bot(bot_username=bot_username)
            if bot_info.user.balance<=0 and (agen_type=='auto' or agen_type=='half-auto'):
                await callback.message.edit_text(f"❗️❗️❗️На вашем балансе нет средств.\n\nСвяжитесь с администратором бота (@{bot_info.user.username}), чтобы пополнить баланс.")
            else:
                if agen_type == 'auto':
                    await callback.message.edit_text(f'{prefix} 🚀 автоматическая обработка.')
                elif agen_type == 'manual':
                    await callback.message.edit_text(f'{prefix} ✍️ ручная обработка.')
                elif agen_type == 'half-auto':
                    await callback.message.edit_text(f'{prefix} 📝 полуавтоматическая обработка.')
            is_paused[callback.message.chat.id]= False
        except Exception as e:
            print(f"subbot:sbb_handle_: {e}\n\n{traceback.format_exc()}")
            logging.error(f"subbot:sbb_handle_: {e}\n\n{traceback.format_exc()}")
            

async def mess_answering(message: types.Message, state: FSMContext, bot: MyBot):
    try: 
        question = (await state.get_data())['question_id']
    except:
        bot.send_message('ℹ️ Бот был обновлён. Если вы собирались ответить на другое сообщение, нажмите "Отмена", но можете и ответить на это сообщение.')    
        question = await get_one_wbfeed_last(is_answering=True, answering_chat_id=message.from_user.id)
        mess_ids = [[m.chat_id, m.mess_id] for m in await get_all_wbfeedanswer(question_id=question.id)]
        await bot.edit_messages_beside(f"✔️ Другой менеджер уже отвечает на это сообщение:\n\n{question.feed_mess}", message.message_id, mess_ids)
        temp_answer = await get_one_wbfeedanswer_last(chat_id=int(message.chat.id), mess_id=message.message_id)
        request_mess = await bot.send_message(message.from_user.id, text=f'✍️ Введите ответ на это сообщение.\n\n📄 {question.feed_mess}', reply_markup=await cancel_answer_sbb_kb(question_id=question.id))
        is_paused[message.chat.id] = True
        await update_wbfeedanswer(id=temp_answer.id, mess_id=request_mess.message_id)
        await state.update_data(question_id=question.id)
        await state.set_state(FeedState.mess_answering)
        return
    bot_info = await get_one_bot(bot_username=(await bot.get_me()).username)
    success = await answer_for_feedback(wb_token=bot_info.wb_token, feedback_id=question.feed_id, text=message.text)
    if success:
        await bot.send_message(message.from_user.id, f'✅ Ответ на это сообщение отправлен:\n\n{question.feed_mess}\n\n✉️ {message.text}')
        await update_wbfeed(id=question.id, is_answering=False, feed_ans=message.text, ai_usage='manual')
        mess_ids= []
        mess_ids = [[m.chat_id, m.mess_id] for m in await get_all_wbfeedanswer(question_id=question.id)]    
        await bot.edit_messages_beside(f"✔️ На это сообщение уже дан ответ:\n\n{question.feed_mess}\n\n✉️ {message.text}", None, mess_ids) 
        is_paused[message.chat.id] = False
        await state.clear()
    else:
        
        await bot.send_message(message.from_user.id, 'Что-то пошло не так. Попробуйте ещё раз.\n\nВведите сообщение:', await wb_ans_manual_kb(answer_id=question.id))
        await state.set_state(FeedState.mess_answering)
        
is_notified_auth_list = {}
is_notified_balance_list = {}

async def nmain_loop(bot: MyBot, main_bot: MyBot):
    bot_username = (await bot.get_me()).username
    n = await get_bot_row(bot_username=bot_username)
    bot_info = await get_one_bot(bot_username=bot_username)
    is_notified_auth_list[bot_info.chat_id] = False
    is_notified_balance_list[bot_info.chat_id] = False
    while True:
        user = await get_user(bot_info.chat_id)
        if is_notified_balance_list[bot_info.chat_id]==False and user.balance < 100:
            is_notified_balance_list[bot_info.chat_id] = True
            try:
                await main_bot.send_message(chat_id=bot_info.chat_id, text='❗️❗️❗️Баланс менее 100 р. Для продолжения пользования платными функциями бота, пополните баланс. 💵 Воспользуйтесь командой /pay')
                logging.info(f"MESSAGE SENT {bot_info.chat_id} баланс меньше 100 USER NOTIFIED")
            except: logging.error("MESSAGE NOT SENT Баланс мельше 100 р")
            logging.info(f"nmain_loop:{bot_info.chat_id} баланс меньше 100 USER NOTIFIED")
        elif user.balance >= 100:
            is_notified_balance_list[bot_info.chat_id] = False        
        try:
            if len(bot_list[n]['managers'])<=1 and is_paused[bot_list[n]['managers'][0]]==True:
                print('ALL MANAGERS PAUSED\n\n')
                await asyncio.sleep(60)
                continue
        except: pass
        ping = await get_ping(bot_info.wb_token)
        if is_notified_auth_list[bot_info.chat_id] == False and ping == 401:
            await main_bot.send_message(bot_info.chat_id, 'Токен ВБ не авторизован. Поменяйте токен. Не забудьте дать разрешения на запись и категории: "Отзывы" и "Аналитика".\n')       
            is_notified_auth_list[bot_info.chat_id] = True
        elif is_notified_auth_list == True and ping == 200:
            await main_bot.send_message(bot_info.chat_id, 'Токен ВБ авторизован.\n')
            is_notified_auth_list[bot_info.chat_id] = False
        if ping == 401:
            await asyncio.sleep(60)
            continue
        new_messages = await get_all_wbfeed(bot_username=bot_username, is_new=True)
        print("\nnNMAIN LOOP: " + str(len(new_messages)))
        automated_type = {}
        automated_type['all'] = 'manual'
        for manag in bot_list[n]['managers']:
            automated_type[manag] = (await get_one_register(chat_id=manag)).automated_type
            if automated_type[manag] == 'auto':
                automated_type['all'] = 'auto'
                break
            elif automated_type[manag] == 'half-auto':
                automated_type['all'] = 'half-auto'
        for mess in new_messages:
            not_paused_managers = []
            user = await get_user(bot_info.chat_id)
            try:
                count_paused = 0
                for manag in bot_list[n]['managers']:
                    try:
                        if is_paused[manag]==True:
                            count_paused+=1
                        else:
                            not_paused_managers.append(manag)
                    except:not_paused_managers.append(manag)
                if count_paused >= len(bot_list[n]['managers']):
                    await asyncio.sleep(60)
                    break
                generated = ""
                total_tokens = 0
                BALANCE_IS_OVER = (f"❗️❗️❗️Внимание! На балансе менее 100 р. Свяжитесь с администратором бота, чтобы он пополнил баланс. @{user.username}\n\n" if user.balance<=100 and user.balance>0 else "")
                BALANCE_IS_OVER = (f"❗️❗️❗️Внимание! У вас нет средств на балансе. Свяжитесь с администратором бота, чтобы он пополнил баланс. @{user.username}\n\n" if user.balance<=0 else "")
                whole_msg = (str(mess.feed_mess) + '\n\n' if str(mess.feed_mess) else "")+ (str(mess.materials_links) + '\n\n' if str(mess.materials_links) else "") + str(mess.createdDate) + '\n\nОценка: ' + str(mess.valuation)
                if automated_type['all'] == 'half-auto' or automated_type['all'] == 'auto':
                    if user.balance>0:
                        generated, total_tokens = await generate_answer(whole_msg, bot_info, mess.customer_name)
                mess_ids = []
                if automated_type['all'] == 'auto' and user.balance>0:
                    msg = await bot.send_messages(user_list=not_paused_managers, text=BALANCE_IS_OVER+whole_msg+'\n\n🚀 Ответ: \n'+generated)
                    success = await answer_for_feedback(wb_token=bot_info.wb_token, feedback_id=mess.feed_id, text=generated)
                    added_data = await add_answer_data(chat_id=bot_list[n]['managers'][0], text=generated, question_id=mess.id, total_tokens=total_tokens)
                    if success:
                        await update_wbfeed(id=mess.id, is_answering=False, feed_ans=generated)
                    else:
                        for manag in bot_list[n]['managers']:
                            try:
                                if is_paused[manag]:
                                    continue
                            except KeyError: pass
                        await bot.send_messages(user_list=bot_list[n]['managers'], text=f'Что-то пошло не так. На сообщение: \n{whole_msg}\n\n Ответить не получилось. Попробуйте ещё раз. \n\n🚀 Ответ:\n{added_data.text}', reply_markup=await wbfeedsent_kb(answer_id=added_data.id))
                else:    
                    for manag in bot_list[n]['managers']:
                        try:
                            if len(bot_list[n]['managers'])>1 and is_paused[manag]==True:
                                print(f'{manag} PAUSED\n\n')
                                continue
                        except KeyError: logging.info(f'subbot:nmain_loop:319 KeyError({manag}) (is_paused empty){is_paused}')
                        try:
                            print('\n\nis paused: '+str(is_paused[manag])+'\n\n')
                        except: print(f'is paused {is_paused}\n\n')
                        added_data_id = (await add_answer_data(chat_id=manag, text=generated, question_id=mess.id, total_tokens=total_tokens)).id
                        if automated_type[manag]== 'half-auto' and user.balance>0:
                            msg = await bot.send_message(manag, text=whole_msg+'\n\n✨ Ответ может быть: ✨\n'+generated, reply_markup=await wbfeedsent_kb(answer_id=added_data_id))  
                        else:
                            msg = await bot.send_message(manag, text=whole_msg, reply_markup=await wb_ans_manual_kb(question_id=mess.id))

                        await update_wbfeedanswer(id=added_data_id, mess_id= msg.message_id)
                        mess_ids.append(int(msg.message_id))
                    await update_wbfeed(id=mess.id, is_new = False, mess_ids=mess_ids)
                await asyncio.sleep(1.5)
            except Exception as e:
                print(f'Ошибка в main_loop: {e}\n\n{traceback.print_exc()}\n')
                logging.error(f"nmain_loop: {e}\n\n{traceback.print_exc()}\n")
        if await get_one_bot(bot_username=bot_username) is None:
            logging.info(f"Bot {bot_username} not found in db. Exiting...")
            bot.session.close()
            break
            
        await asyncio.sleep(60)