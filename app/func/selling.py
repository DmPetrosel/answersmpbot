from create_bot import dp, bot
from aiogram import types,  Dispatcher, handlers, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.state import State
from aiogram.filters import Command, StateFilter
from varname.helpers import Wrapper
import configparser
from db.set import *
from db.get import *
import errh
from functools import partial
import logging
from keyboard.basic_kb import *
from func.marketer import *

class Form(StatesGroup):
    first_name = State()
    username = State()
    promocode = State()

usr = {}
user_obj = {}

async def start(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Привет, я бот для автоответов на ВБ\nПродолжая пользоваться ботом, вы соглашаетесь на обработку персональных данных.")
    if(await get_user(chat_id=message.from_user.id)):
        await bot.send_message(message.from_user.id, "Вы уже зарегистрированы! Здесь будут кнопки с меню. ")
        user_obj[message.from_user.id] = await get_user(message.from_user.id)
        if user_obj[message.from_user.id].marketer == True:
            print('Condition with is marketer passed ==============')
            await marketer(message.from_user.id)
    else:
        usr[message.from_user.id] = {}
        await registration(message, state)

async def registration(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Давайте зарегистрируемся!")
    usr[message.from_user.id]['marketer'] = False
    usr[message.from_user.id]['promocode'] = None

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
        try:
            await bot.send_message(message.from_user.id, f"Введите промокод.", reply_markup=no_promo_kb())
            await state.set_state("promocode")
        except Exception as e:
            logging.error(f"{e}")
    elif await state.get_state() == 'promocode':   
        usr[message.from_user.id]['promocode'] = var.lower()
        try:
            if var.lower() == 'ямаркетолог' or var.lower() == 'я маркетолог':
                usr[message.from_user.id]['marketer'] = True
                usr[message.from_user.id]['promocode'] = 'ямаркетолог'
                await write_registration(message.from_user.id)
                await state.clear()
            else:
                usr[message.from_user.id]['price'] = await errh.handle_errors(partial(get_bot_price, usr[message.from_user.id]['promocode']))
                if usr[message.from_user.id]['price'] == None:
                    await bot.send_message(message.from_user.id, 'Промокод не найден, попробуйте ещё раз: /start')
                    await state.set_state("promocode")
                else:
                    await write_registration(message.from_user.id)
                    await state.clear()
        except Exception as e:
            logging.error(f"{e}")
    else:
        await bot.send_message(message.from_user.id, 'Что-то пошло не так, попробуйте ещё раз: /start')
    

async def write_registration(chat_id):
    logging.info(f"REGISTRATION DATA: {usr[chat_id]['username']}, {usr[chat_id]['first_name']}, {usr[chat_id]['promocode']}, {usr[chat_id]['marketer']}")
    if await errh.handle_errors(partial(add_user,chat_id=chat_id, username=usr[chat_id]['username'], first_name=usr[chat_id]['first_name'], promocode=usr[chat_id]['promocode'], marketer=usr[chat_id]['marketer'])):
        await bot.send_message(chat_id, 'Регистрация прошла успешно')
    else:
        await bot.send_message(chat_id, str('Регистрация не удалась: \nВозможно, вы уже зарегистрированы'))
    user_obj[chat_id] = await get_user(chat_id)
    if user_obj[chat_id].marketer == True:
        await marketer(chat_id)
    else:
        print("FAAAAAAAAAAAALESEEEEEEEEEEEE=====================")
    return
async def callback_selling(callback: types.CallbackQuery):
    config = configparser.ConfigParser()
    config.read('config.ini')
    if callback.data == 'no_promo_call':
        price = config.get('price', 'default')
        usr[callback.from_user.id]['price'] = price
        await promo_continue(callback.from_user.id, price)
    elif callback.data == 'pay_call':
        await bot.send_message(callback.from_user.id, f"Оплата по ссылке {usr[callback.from_user.id]['price']}₽: <a href='yookassa.ru'>ЮКасса</a>", parse_mode='html')
async def promo_continue(chat_id, price):
    await write_registration(chat_id)
    await bot.send_message(chat_id, f'Ваша цена: {price}', reply_markup=promo_continue_kb())

def register_selling_handlers(dp):
    dp.callback_query.register(callback_selling, lambda c: c.data in ('no_promo_call', 'pay_call'))
    dp.message.register(start, Command(commands=("start", "restart", "help")), State(state="*"))
    dp.message.register(get_answer_reg, StateFilter('first_name', 'username', 'promocode'))
    # dp.callback_query.register(callback_selling, StateFilter('no_promo_call', 'pay_call' ))