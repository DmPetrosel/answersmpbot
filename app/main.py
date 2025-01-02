from aiogram import Bot, Dispatcher, types
import asyncio
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
print(config['bot']['token'])
bot = Bot(token=config['bot']['token'])
dp = Dispatcher(bot=bot)
async def main():
    await bot.send_message(chat_id=config['bot']['owner_id'],text='Bot started')
    await dp.start_polling(bot)

asyncio.run(main())