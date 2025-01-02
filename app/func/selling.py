from create_bot import dp, bot
from aiogram import types,  Dispatcher, handlers
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.state import State
from aiogram.filters import Command, StateFilter
from varname.helpers import Wrapper

class Form(StatesGroup):
    name = State()
    lastname = State()
    username = State()
    ans_state = State()

class usr:
    name = ""
    lastname = ""
    username = ""
    
    

async def start(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Привет, я бот для автоответов на ВБ")
    await registration(message, state)

async def registration(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Давайте зарегистрируемся!")
    usr.username = message.from_user.username
    if usr.username == None: 
        await bot.send_message(message.from_user.id, "Введите никнейм")
        await state.set_state("username")
    else:
        await bot.send_message(message.from_user.id, "Введите имя")
        await state.set_state("name")
    

async def get_answer(message : types.Message, state: FSMContext):
    var = message.text
    if await state.get_state() == 'username':
        usr.username = var
        await bot.send_message(message.from_user.id, "Введите имя")
        await state.set_state("name")
    elif await state.get_state() == 'name':
        usr.name = var
        await bot.send_message(message.from_user.id, 'Введите фамилию')
        await state.set_state("lastname")
    elif await state.get_state() == 'lastname':
        usr.lastname = var
        await bot.send_message(message.from_user.id, f'Ваши данные {usr.username}, {usr.name}, {usr.lastname}')
        await state.clear()
    else:
        await bot.send_message(message.from_user.id, 'Что-то пошло не так')
    return var

def register_selling_handlers(dp):
    dp.message.register(start, Command(commands=("start", "restart", "help")), State(state="*"))
    dp.message.register(get_answer, StateFilter('name', 'username', 'lastname'))