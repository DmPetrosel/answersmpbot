from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from db.get import *

async def wbfeedsent_kb(answer_id):
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    kb.inline_keyboard.append([InlineKeyboardButton(text='Ответить', callback_data=f'sbb_wbfeedsent_yes_{answer_id}')])
    kb.inline_keyboard.append([InlineKeyboardButton(text='Сгенерировать новый', callback_data=f'sbb_wbfeedsent_gen_{answer_id}')])
    kb.inline_keyboard.append([InlineKeyboardButton(text='Свой ответ', callback_data=f'sbb_wbfeedsent_oneself_{answer_id}')])