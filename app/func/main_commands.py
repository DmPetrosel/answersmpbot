from create_bot import *
from aiogram import types,  Dispatcher, handlers, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from func.selling import *
from func.states import *
async def add_bot(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Создайте бот в @botfather и вставьте сюда токен бота.', reply_markup=how_to_create_bot_kb())
    await state.set_state("get_bot_token")

async def delete_bot(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Выберете бота для удаления', reply_markup=delete_bot_list_kb(int(message.from_user.id)))