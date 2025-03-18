from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from db.get import *

def marketer_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Мои промокоды', callback_data='my_promos')],
        [InlineKeyboardButton(text='Создать новый', callback_data='create_promo')],
    ])

async def add_manager_list_kb(bot_username :str):
    bt = await get_one_bot(bot_username=bot_username)
    not_approved_managers = await get_all_register(bot_username=bot_username, approve=False)
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    if not_approved_managers:
        for manager in not_approved_managers:
            kb.inline_keyboard.append([InlineKeyboardButton(text=manager.username, callback_data=f'mcadd_manager_next_{bt.id}_{manager.id}')])
        kb.inline_keyboard.append([InlineKeyboardButton(text='Обновить список', callback_data=f'mcadd_manager_choose_them_{bt.id}')])
    kb.inline_keyboard.append([InlineKeyboardButton(text='Отмена', callback_data='mccancel_call')])
    return kb        

def choose_bot_for_add_manager_kb(chat_id:str):
    user_bot_list = get_all_bots(chat_id=chat_id)
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    if user_bot_list:
        for ibot in user_bot_list:
            kb.inline_keyboard.append([InlineKeyboardButton(text=ibot.username, callback_data=f'mcadd_manager_choose_them_{ibot.id}')])
    kb.inline_keyboard.append([InlineKeyboardButton(text='Отмена', callback_data='mccancel_call')])
    return kb        
