import asyncio
import configparser
from func.selling import register_selling_handlers
from create_bot import *
from func.selling import *
import logging
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', encoding='utf-8', filemode='a', filename='data/log.log')
config = configparser.ConfigParser()
config.read('config.ini')
register_selling_handlers(dp)




async def main():
    await bot.send_message(chat_id=config['bot']['owner_id'],text='Bot started')
    await dp.start_polling(bot, skip_updates=False)


asyncio.run(main())
event_loop.run_forever()