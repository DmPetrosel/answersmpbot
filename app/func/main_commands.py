from create_bot import *
from aiogram import types,  Dispatcher, handlers, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from func.selling import *
from func.states import *
from aide import MyBot
async def add_bot(message: types.Message, state: FSMContext, bot: MyBot):
    await bot.send_message(message.from_user.id, 'Создайте бот в @botfather и вставьте сюда токен бота.', reply_markup=how_to_create_bot_kb())
    await state.set_state("get_bot_token")

async def delete_bot_ask(message: types.Message, state: FSMContext, bot: MyBot):
    await bot.send_message(message.from_user.id, 'Выберете бота для удаления', reply_markup=delete_bot_list_kb(int(message.from_user.id)))



async def add_manager(message: types.Message, state: FSMContext, bot: MyBot):
    await bot.send_message(message.from_user.id, 'Выберете бота для добавления менеджера', reply_markup=choose_bot_for_add_manager_kb(int(message.from_user.id)))

async def delete_manager(message: types.Message, state: FSMContext, bot: MyBot):
    await bot.send_message(message.from_user.id, 'Выберете бота для удаления менеджера', reply_markup=delete_manager_list_kb(int(message.from_user.id)))