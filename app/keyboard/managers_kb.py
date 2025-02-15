from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from db.get import *

async def wbfeedsent_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    kb.inline_keyboard.append([InlineKeyboardButton(text='Ответить', callback_data='sbb_wbfeedsent_yes')])
    kb.inline_keyboard.append([InlineKeyboardButton(text='Сгенерировать новый', callback_data='sbb_wbfeedsent_gen')])
    kb.inline_keyboard.append([InlineKeyboardButton(text='Свой ответ', callback_data='sbb_wbfeedsent_oneself')])