from main import dp, bot
from aiogram import types,  Dispatcher, handlers



async def start(message: types.Message):
    await bot.send_message(message.from_user.id, "Привет, я бот для автоответов на ВБ")




def register_selling_handlers(dp):
    dp.register_message_handler(start, commands=("start", "restart", "help"), state="*")