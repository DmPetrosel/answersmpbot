import aiogram.filters
from create_bot import *
from aiogram import types,  Dispatcher, handlers, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.filters.command import CommandObject
import configparser
from db.set import *
from db.update import *
from db.get import *
import errh
from functools import partial
import logging
from keyboard.basic_kb import *
from func.marketer import *
from func.states import *
from db.session import Base
import aiogram

usr = {}
user_obj = {}
new_bot = {} # chat_id, token, bot_username, company_name, samples_ans, wb_token

async def start(message: types.Message, command: CommandObject, state: FSMContext):
    try:
        await bot.send_message(message.from_user.id, "Привет, я бот для автоответов на ВБ\nПродолжая пользоваться ботом, вы соглашаетесь на обработку персональных данных.")
        if(await get_user(chat_id=message.from_user.id)):
            await bot.send_message(message.from_user.id, "Вы уже зарегистрированы! Здесь будут кнопки с меню. ")
            user_obj[message.from_user.id] = await get_user(message.from_user.id)
            if user_obj[message.from_user.id].marketer == True:
                print('Condition with is marketer passed ==============')
                await marketer(message.from_user.id)
        else:

            usr[message.from_user.id] = {}
            usr[message.from_user.id]['promocode'] = None
            promo_obj = None
            try:
                arg = command.args
                print('=====', arg)
                if arg is not None:
                    promo_obj = await get_promo_by_kwargs(referal=arg)
            except Exception as e:
                print("Exception ", e)
            if promo_obj:
                usr[message.from_user.id]['referal'] = promo_obj.referal
                usr[message.from_user.id]['expire_date'] = promo_obj.expire_date
                usr[message.from_user.id]['promocode'] = promo_obj.promocode
                usr[message.from_user.id]['price'] = promo_obj.price
                print("Промокод найден")
            if promo_obj == None and arg is not None:
                await bot.send_message(message.from_user.id, "Промокод не найден! Вы сможете ввести его после имени.")
                usr[message.from_user.id]['referal'] = None
                usr[message.from_user.id]['expire_date'] = None
                usr[message.from_user.id]['promocode'] = None  
                usr[message.from_user.id]['price'] = None
            if promo_obj and promo_obj.expire_date != None and datetime.strptime(usr[message.from_user.id]['expire_date'], '%d.%m.%Y') < datetime.now():
                await bot.send_message(message.from_user.id, "Ваш промокод просрочен!")
                usr[message.from_user.id]['referal'] = None
                usr[message.from_user.id]['expire_date'] = None
                usr[message.from_user.id]['promocode'] = None
                usr[message.from_user.id]['price'] = None

            await registration(message, state)
    except Exception as e:
        logging.error(f"При запуске бота ошибка {e}")
async def registration(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Давайте зарегистрируемся!")
    usr[message.from_user.id]['marketer'] = False

    usr[message.from_user.id]['username'] = message.from_user.username
    if usr[message.from_user.id]['username'] == None: 
        await bot.send_message(message.from_user.id, "Введите никнейм")
        await state.set_state("username")
    else:
        await bot.send_message(message.from_user.id, "Введите имя")
        await state.set_state("first_name")
    

async def get_answer_reg(message : types.Message, state: FSMContext):
    var = message.text
    if await state.get_state() == 'username':
        usr[message.from_user.id]['username'] = var
        await bot.send_message(message.from_user.id, "Введите имя")
        await state.set_state("name")
    elif await state.get_state() == 'first_name':
        usr[message.from_user.id]['first_name'] = var
        if usr[message.from_user.id]['promocode'] == None:
            try:
                await bot.send_message(message.from_user.id, f"Введите промокод.", reply_markup=no_promo_kb())
                await state.set_state("promocode")
            except Exception as e:
                logging.error(f"{e}")
        else:
            await state.clear()
            await write_registration(message.from_user.id)

    elif await state.get_state() == 'promocode':   
        usr[message.from_user.id]['promocode'] = var.lower().strip()
        reg_success = False
        try:
            if var.lower().strip() == 'ямаркетолог' or var.lower().strip() == 'я маркетолог':
                usr[message.from_user.id]['marketer'] = True
                usr[message.from_user.id]['promocode'] = 'ямаркетолог'
                await state.clear()
            else:
                promo_obj = await get_promo_by_kwargs(promocode=usr[message.from_user.id]['promocode'])
                
                usr[message.from_user.id]['price'] = promo_obj.price

                if usr[message.from_user.id]['price'] == None:
                    await bot.send_message(message.from_user.id, 'Промокод не найден, попробуйте ещё раз: /start')
                    await state.set_state("promocode")
                else:
                    await state.clear()
            await write_registration(message.from_user.id)
            
        except Exception as e:
            logging.error(f"{e}")
    else:
        await bot.send_message(message.from_user.id, 'Что-то пошло не так, попробуйте ещё раз: /start')
    

async def write_registration(chat_id):
    logging.info(f"REGISTRATION DATA: {usr[chat_id]['username']}, {usr[chat_id]['first_name']}, {usr[chat_id]['promocode']}, {usr[chat_id]['marketer']}")
    if await add_user(chat_id=chat_id, username=usr[chat_id]['username'], first_name=usr[chat_id]['first_name'], promocode=usr[chat_id]['promocode'], marketer=usr[chat_id]['marketer']):
        await bot.send_message(chat_id, 'Регистрация прошла успешно')
    else:
        await bot.send_message(chat_id, str('Регистрация не удалась: \nВозможно, вы уже зарегистрированы'))
        return False
    user_obj[chat_id] = await get_user(chat_id)
    if user_obj[chat_id].marketer == True:
        await marketer(chat_id)
    else:
        await promo_continue(chat_id, usr[chat_id]['price'])
    return True
async def callback_selling(callback: types.CallbackQuery, state: FSMContext):
    config = configparser.ConfigParser()
    config.read('config.ini')
    if callback.data == 'no_promo_call':
        price = config.get('price', 'default')
        usr[callback.from_user.id]['price'] = price
        await write_registration(callback.from_user.id)
    elif callback.data == 'pay_call':
        await bot.send_message(callback.from_user.id, f"Оплата по ссылке {usr[callback.from_user.id]['price']}₽: <a href='yookassa.ru'>ЮКасса</a>", parse_mode='html')
        await bot.send_message(callback.from_user.id, f"Продолжить без оплаты.", reply_markup=without_payment_kb())
    elif callback.data == 'no_pay_call':
        await bot.send_message(callback.from_user.id, f"Без оплаты ботом можно пользоваться 7 дней.")
        await bot.send_message(callback.from_user.id, 'Создайте бот в @botfather и вставьте сюда токен бота.', reply_markup=how_to_create_bot_kb())
        await state.set_state("get_bot_token")
    elif callback.data == 'how_to_create_bot_call':
        await bot.send_message(callback.from_user.id, 'https://core.telegram.org/bots')
        await state.set_state("get_bot_token")
    elif callback.data == 'cancel_call':
        await callback.message.edit_text('Действие отменено.\n\nДля управления воспользуйтесь командами')
    elif callback.data.startswith('del_bot_next_'):
        await callback.message.edit_text('Вы уверены, что хотите удалить бота?', reply_markup=del_bot_kb(int(callback.data.split('_')[-1])))
    elif callback.data.startswith('del_bot_yes_'):
        await delete_bot(int(callback.data.split('_')[-1]))
        await bot.send_message(callback.from_user.id, 'Бот удалён. \n\nДля управления воспользуйтесь командами (меню)')
    elif callback.data.startswith('add_manager_choose_them_'):
        tbot_data = get_one_bot(chat_id = int(callback.data.split('_')[-1]))
        await bot.send_message(callback.from_user.id, f'Выберете менеджера из списка. Если его в списке нет, вероятно, он не нажал кнопу старт в боте {tbot_data.bot_username}', reply_markup=add_manager_list_kb(tbot_data.bot_username))    
    elif callback.data.startswith('add_manager_next_'):
        success = await update_register(id=callback.data.split('_')[-1], approved = True)
        if success:
            await bot.send_message(callback.from_user.id, 'Менеджер добавлен.')
        else:
            await bot.send_message(callback.from_user.id, 'Что-то пошло не так, попробуйте ещё раз.')
            
    else:
        await bot.send_message(callback.from_user.id, 'Что-то пошло не так, попробуйте ещё раз: /start')
    
async def promo_continue(chat_id, price):
    await bot.send_message(chat_id, f'Ваша цена: {price}', reply_markup=promo_continue_kb())

async def get_bot_token(message: types.Message, state: FSMContext):
    list_n = await bot_init(token=message.text.strip(), chat_id=int(message.from_user.id), managers=[message.from_user.id])
    new_bot[message.from_user.id] = {} # chat_id, token, bot_username, company_name, samples_ans, wb_token

    new_bot[message.from_user.id]['chat_id'] = int(message.from_user.id)
    new_bot[message.from_user.id]['token'] = message.text.strip()
    if list_n != None:
        await bot.send_message(message.from_user.id, f'Токен бота: {message.text.strip()}\n\n Теперь введите API-токен WB.\nОн должен быть сделан с возможностью записи чтобы можно было отвечать на WB отзывы.')
        await bot_list[list_n]['bot'].send_message(message.from_user.id, f'Поздравляем, бот подключён!')
        await add_bot_info(new_bot[message.from_user.id])
        # TODO check if it correct and all fields exists
        await add_register(chat_id=int(message.from_user.id), username= message.from_user.username, name = message.from_user.first_name, bot_username = bot_list[n]['bot_username'])
        await state.set_state('get_wb_token')
    else:
        await bot.send_message(message.from_user.id, f'Бот не подключён. Попробуйте ещё раз. \n\nВведите токен бота: ')
        await state.set_state("get_bot_token")
async def get_wb_token(message: types.Message, state: FSMContext):
    list_n = await get_bot_row(chat_id=int(message.from_user.id))
    new_bot[message.from_user.id]['wb_token'] = message.text.strip()
    wb_token = message.text.strip()
    if wb_token:
        await bot.send_message(message.from_user.id, f'API-токен WB: {message.text.strip()}')
        await bot.send_message(message.from_user.id, f'Поздравляем, бот подключён!')
        bot_list[list_n]['wb_token'] = wb_token
        await update_bot_info(new_bot[message.from_user.id], chat_id=int(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, f'Что-то пошло не так, возможно, проблема с токеном.')


def register_selling_handlers(dp):
    dp.callback_query.register(callback_selling, lambda c: c.data in ('no_promo_call', 'pay_call', 'no_pay_call', 'how_to_create_bot_call'))
    dp.message.register(start, Command(commands=("start", "restart")), State(state="*"))
    dp.message.register(get_answer_reg, StateFilter('first_name', 'username', 'promocode'))
    dp.message.register(get_bot_token, StateFilter('get_bot_token'))
    dp.message.register(get_wb_token, StateFilter('get_wb_token'))
    # dp.callback_query.register(callback_selling, StateFilter('no_promo_call', 'pay_call' ))