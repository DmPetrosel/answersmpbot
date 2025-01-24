from aiogram import types
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup

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
    