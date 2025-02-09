import asyncio
import configparser
from func.selling import register_selling_handlers
from create_bot import *
from func.selling import *
import logging
import threading
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', encoding='utf-8', filemode='a', filename='data/log.log')
config = configparser.ConfigParser()
config.read('config.ini')

async def main():
    await init_when_restart()
    tasks.append(asyncio.create_task(main_bot()))
    await asyncio.gather(*tasks)

asyncio.run(main())


# def run_event_loop(loop):
#     asyncio.set_event_loop(loop)
#     loop.run_forever()



# thread = threading.Thread(target=my_event_loop.run_forever, daemon=False)
# thread.start()