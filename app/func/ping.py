import aiohttp
import logging
import sys
from db.get import *
import asyncio



async def get_ping(wb_token : str):
    # link = "https://feedbacks-api.wildberries.ru/ping"
    headers = {"Authorization": wb_token}   
    link = "https://feedbacks-api-sandbox.wildberries.ru/ping"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(link, headers=headers) as resp:
                if resp.status == 200:
                    logging.info(f"CONNECTED, STATUS = {resp.status}")
                elif resp.status == 401:
                    logging.error(f"CONNECTION ERROR: UNAUTHORIZED. STATUS = {resp.status}:\n{await resp.json()}")
                else:
                    logging.error(f"CONNECTION ERROR. STATUS = {resp.status}\n{await resp.json()}")
                return resp.status
        except Exception as e:
            logging.error(f"CONNECTION ERROR: {e}")
            return None

async def ping_main():
    logging.basicConfig(level="INFO")
    wb_token = (await get_all_bots())[0].wb_token
    status = await get_ping(wb_token)
    print("CODE: ", status)

if __name__ == "__main__":
    asyncio.run(ping_main())