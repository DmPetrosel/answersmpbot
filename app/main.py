import asyncio
import configparser
from func.selling import register_selling_handlers
from create_bot import bot,dp
config = configparser.ConfigParser()
config.read('config.ini')
register_selling_handlers(dp)
async def main():
    await bot.send_message(chat_id=config['bot']['owner_id'],text='Bot started')
    await dp.start_polling(bot)

asyncio.run(main())