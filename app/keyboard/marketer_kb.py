from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup

def marketer_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Мои промокоды', callback_data='my_promos')],
        [InlineKeyboardButton(text='Создать новый', callback_data='create_promo')],
    ])