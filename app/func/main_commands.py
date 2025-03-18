from aiogram import types,  Dispatcher, handlers, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from func.selling import *
from func.states import *
from keyboard.basic_kb import *
from func.marketer_module import *
from aide import MyBot
async def add_bot(message: types.Message, state: FSMContext, bot: MyBot):
    await state.clear()
    await bot.send_message(message.from_user.id, 'Создайте бот в @botfather и вставьте сюда токен бота.', reply_markup=how_to_create_bot_kb())
    await state.set_state("get_bot_token")

async def delete_bot_ask(message: types.Message, state: FSMContext, bot: MyBot):
    await state.clear()
    await bot.send_message(message.from_user.id, 'Выберете бота для удаления', reply_markup=await delete_bot_list_kb(int(message.from_user.id)))



async def add_manager(message: types.Message, state: FSMContext, bot: MyBot):
    await state.clear()
    await bot.send_message(message.from_user.id, 'Выберете бота для добавления менеджера', reply_markup=await choose_bot_for_add_manager_kb(int(message.from_user.id)))

async def delete_manager(message: types.Message, state: FSMContext, bot: MyBot):
    await state.clear()
    await bot.send_message(message.from_user.id, 'Выберете бота для удаления менеджера', reply_markup=await delete_manager_choose_bot_list_kb(int(message.from_user.id)))

async def share_command(message: types.Message, state: FSMContext, bot: MyBot):
    await state.clear()
    await marketer(message, bot=bot)
    return