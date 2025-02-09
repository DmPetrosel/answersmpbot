from aiogram.dispatcher.middlewares.base import BaseMiddleware
from db.get import *
from aiogram import types, Bot
from aide import MyBot
from configparser import ConfigParser
from keyboard.basic_kb import *
from typing import Any, Callable, Dict, Awaitable

msg_send_data = {}

class MyMiddleware(BaseMiddleware):
    config = ConfigParser()
    def __init__(self, bot: MyBot):
        self.bot = bot
    async def help(self, message: types.Message):
        await self.bot.send_message(message.from_user.id, f"Если что-то случилось или есть вопросы, \n\nнапишите {config.get('support', 'support')}")
    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.Message,
        data: Dict[str, Any],
    ) -> Any:  # pragma: no cover
        if event.text == '/help':
            await self.help(event)
        return await handler(event, data)

class NMiddlewareMessage(BaseMiddleware):
    def __init__(self, bot: MyBot):
        self.bot = bot
    config = ConfigParser()
    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.Message,
        data: Dict[str, Any],
    ):
        if event.text == '/help':
            config.read('config.ini')
            await self.bot.send_message(event.from_user.id, f"Если что-то случилось или есть вопросы, \n\nнапишите {config.get('support', 'support')}")
        else:
            user = await get_one_register(chat_id=event.from_user.id)
            config.read('config.ini')
            if not user:
                await self.bot.send_message(event.from_user.id, "Пожалуйста, нажмите /start , чтобы начать.")
            elif user and user.approve == False:
                bot_username = (await self.bot.get_me()).username
                bot_info = await get_one_bot(bot_username=bot_username)
                await self.bot.send_message(event.from_user.id, f"Вас не добавили как менеджера в основном боте. Пожалуйста, дождитесь, когда владелец добавит вас в боте {config.get('bot','link')}. Вы можете отправить ему следующее сообщение: ")
                msg_send_data[event.from_user.id] = f"Привет, добавьте меня в бот {bot_username} как менеджера с помощью команды /addm . Мой username -- {event.from_user.username}. "
                await self.bot.send_message(event.from_user.id, msg_send_data[event.from_user.id])
                await self.bot.send_message(event.from_user.id, "Отправить владельцу бота.",reply_markup=send_to_owner_kb(bot_info.chat_id))
        return await handler(event, data)
class NMiddlewareCallback(BaseMiddleware):
    def __init__(self, main_bot: MyBot, nbot: MyBot):
        self.mbot = main_bot
        self.nbot = nbot
    config = ConfigParser()
    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        callback: types.CallbackQuery,
        data: Dict[str, Any],
    ):
        user = await get_one_register(chat_id=callback.from_user.id)
        config.read('config.ini')
        if callback.data.startswith("send_to_owner_yes_"):
            await self.mbot.send_message(callback.data.split('_')[1], msg_send_data[callback.from_user.id])
        elif callback.data == 'subcancel_call':
            callback.message.edit_text("Отмена")

        elif user and user.approve == False:
            bot_username = (await self.nbot.get_me()).username
            bot_info = await get_one_bot(bot_username=bot_username)
            await self.nbot.send_message(callback.from_user.id, f"Вас не добавили как менеджера в основном боте. Пожалуйста, дождитесь, когда владелец добавит вас в боте {config.get('bot','link')}. Вы можете отправить ему следующее сообщение: ")
            await self.nbot.send_message(callback.from_user.id, f"Привет, добавьте меня в бот {bot_username} как менеджера с помощью команды /addm . Мой username -- {callback.from_user.username} ")
            await self.nbot.send_message(callback.from_user.id, "Отправить владельцу бота.", reply_markup=send_to_owner_kb(bot_info.chat_id))
        return await handler(callback, data)