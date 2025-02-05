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

def delete_bot_list_kb(chat_id: int):
    user_bots = get_all_bots(chat_id=chat_id)
    if user_bots:
        kb = InlineKeyboardMarkup(inline_keyboard=[])
        for bot in user_bots:
            kb.add(InlineKeyboardButton(text=bot.bot_username, callback_data=f'del_bot_next_{bot.id}'))
        kb.add(InlineKeyboardButton(text='Отмена', callback_data='cancel_call'))
        return kb
    else:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Отмена', callback_data='cancel_call')]
        ])
        
def del_bot_kb(bot_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Да, я хочу удалить', callback_data=f'del_bot_yes_{bot_id}'),
        InlineKeyboardButton(text='Нет, я передумал', callback_data=f'cancel_call')]
    ])
    