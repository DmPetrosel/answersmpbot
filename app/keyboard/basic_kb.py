from aiogram import types
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from db.get import *
def no_promo_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Продолжить без промокода', callback_data='no_promo_call')]
        ])
def promo_continue_kb():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Оплатить', callback_data='pay_call')]])

def without_payment_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Продолжить без оплаты', callback_data='no_pay_call')]
        ])

def how_to_create_bot_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Как создать бота?', callback_data='how_to_create_bot_call')],
        [InlineKeyboardButton(text='Назад', callback_data='pay_call')]
    ])

async def delete_bot_list_kb(chat_id: int):
    user_bots = await get_all_bots(chat_id=chat_id)
    if user_bots:
        kb = InlineKeyboardMarkup(inline_keyboard=[])
        for bot in user_bots:
            kb.inline_keyboard.append([InlineKeyboardButton(text=bot.bot_username, callback_data=f'mcdel_bot_next_{bot.id}')])
        kb.inline_keyboard.append([InlineKeyboardButton(text='Отмена', callback_data='cancel_call')])
        return kb
    else:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Отмена', callback_data='cancel_call')]
        ])
        
def del_bot_kb(bot_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Да, я хочу удалить', callback_data=f'mcdel_bot_yes_{bot_id}'),
        InlineKeyboardButton(text='Нет, я передумал', callback_data=f'cancel_call')]
    ])
    
async def delete_manager_choose_bot_list_kb(chat_id: int):
    user_bots = await get_all_bots(chat_id=chat_id)
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for bot in user_bots:
        kb.inline_keyboard.append([InlineKeyboardButton(text=f'{bot.bot_username}', callback_data=f'mcdel_manager_choose_them_{bot.id}')])
    kb.inline_keyboard.append([InlineKeyboardButton(text='Отмена', callback_data='mccancel_call')])
    return kb

async def del_manager_list_kb(bot_username: str):
    user_managers = await get_all_register(bot_username=bot_username)
    bt = get_one_bot(bot_username=bot_username)
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for manager in user_managers:
        kb.inline_keyboard.append([InlineKeyboardButton(text=manager.username, callback_data=f'mcdel_manager_next_{bt.id}_{manager.id}')])
    kb.inline_keyboard.append([InlineKeyboardButton(text='Отмена', callback_data='mccancel_call')])
    return kb
    
def send_to_owner_kb(owner_chat_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Отправить', callback_data=f'send_to_owner_yes_{owner_chat_id}')],
        [InlineKeyboardButton(text='Отмена', callback_data='subcancel_call')]
    ])
    
async def choose_bot_for_add_manager_kb(chat_id: int):
    user_bots = await get_all_bots(chat_id=chat_id)
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for bot in user_bots:
        kb.inline_keyboard.append([InlineKeyboardButton(text=f'{bot.bot_username}', callback_data=f'mcadd_manager_choose_them_{bot.id}')])
    kb.inline_keyboard.append([InlineKeyboardButton(text='Отмена', callback_data='mccancel_call')])
    return kb