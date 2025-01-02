from aiogram import Bot, Dispatcher, types
import asyncio
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
print(config['bot']['token'])
bot = Bot(token=config['bot']['token'])
dp = Dispatcher(bot=bot)