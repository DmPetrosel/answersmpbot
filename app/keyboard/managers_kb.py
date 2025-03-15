from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from db.get import *

async def wbfeedsent_kb(answer_id):
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    kb.inline_keyboard.append([InlineKeyboardButton(text='Ответить', callback_data=f'sbb_wbfeedsent_yes_{answer_id}')])
    kb.inline_keyboard.append([InlineKeyboardButton(text='Сгенерировать новый', callback_data=f'sbb_wbfeedsent_gen_{answer_id}')])
    kb.inline_keyboard.append([InlineKeyboardButton(text='Свой ответ', callback_data=f'sbb_wbfeedsent_oneself_{answer_id}')])
    return kb

async def cancel_sbb_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    kb.inline_keyboard.append([InlineKeyboardButton(text='Отменить', callback_data='sbb_cancel_call')])
    return kb

async def wb_ans_manual_kb(question_id):
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    kb.inline_keyboard.append([InlineKeyboardButton(text='Сгенерировать ответ', callback_data=f'sbb_wbfeedsent_gen_manual_{question_id}')])
    kb.inline_keyboard.append([InlineKeyboardButton(text='Свой ответ', callback_data=f'sbb_wbfeedsent_oneself_manual_{question_id}')])
    return kb
