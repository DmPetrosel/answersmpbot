from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from db.get import *

async def wbfeedsent_kb(answer_id):
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    kb.inline_keyboard.append([InlineKeyboardButton(text='✅ Ответить', callback_data=f'sbb_wbfeedsent_yes_{answer_id}')])
    kb.inline_keyboard.append([InlineKeyboardButton(text='✨ Сгенерировать новый', callback_data=f'sbb_wbfeedsent_gen_{answer_id}')])
    kb.inline_keyboard.append([InlineKeyboardButton(text='✍️ Свой ответ', callback_data=f'sbb_wbfeedsent_oneself_{answer_id}')])
    return kb

async def cancel_sbb_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    kb.inline_keyboard.append([InlineKeyboardButton(text='Отменить', callback_data='sbb_cancel_call')])
    return kb

async def cancel_answer_sbb_kb(question_id):
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    kb.inline_keyboard.append([InlineKeyboardButton(text='Отменить', callback_data=f'sbb_cancel_answer_call_{question_id}')])
    return kb


async def wb_ans_manual_kb(question_id):
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    kb.inline_keyboard.append([InlineKeyboardButton(text='✨ Сгенерировать ответ', callback_data=f'sbb_wbfeedsent_gen_manual_{question_id}')])
    kb.inline_keyboard.append([InlineKeyboardButton(text='✍️ Свой ответ', callback_data=f'sbb_wbfeedsent_oneself_manual_{question_id}')])
    return kb

async def agen_kb(temporaty_type):
    agen_types = [['🚀 Авто-обработка','auto'], ['📝 С подтверждением','half-auto'], ['✍️ Ручная обработка','manual']]
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for atype in agen_types:
        if temporaty_type == atype[1]:
            tt_name = atype[0]
            continue
        print(f"\nKEYBOARD {atype[1]}")
        kb.inline_keyboard.append([InlineKeyboardButton(text=atype[0], callback_data=f'sbb_handle_{atype[1]}')])
    kb.inline_keyboard.append([InlineKeyboardButton(text=f"Оставить: {tt_name}", callback_data=f'sbb_handle_current_{temporaty_type}')])
    return kb
