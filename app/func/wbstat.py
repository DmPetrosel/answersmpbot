import aiohttp
import asyncio
import json
import requests
import time
import logging
from  threading import Thread
import sys
sys.path.append('../app')
from db.get import *
import random as rand
# base_url = 'https://statistics-api-sandbox.wildberries.ru'
# base_url ='https://seller-analytics-api.wildberries.ru' # prod
base_url ='https://seller-analytics-api.wildberries.ru' # prod

class WBStat:
    def __init__(self, bot_username, 
                  daemon = True):
        self.token = ""
        self.bot_username = bot_username
        self.daemon = daemon
        self.interval = 30
    # async def request_for_stocks(self):
    #     url = f"{base_url}/api/v1/warehouse_remains?groupByNm=true&groupBySubject=true"
    #     headers = {'Authorization': self.token, 'Content-Type': 'application/json'}
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get(url, headers=headers) as response:
    #             if response.status == 200:
    #                 data = await response.json()
    #                 taskId = data.get("data").get('taskId')
    #                 print(f"taskId = {taskId}")
    #                 return taskId
    #             else:
    #                 print(f"request for stock {response.status}")
    #         return None

    # async def check_status(self, taskId):
    #     url = f"{base_url}/api/v1/warehouse_remains/tasks/{taskId}/status"
    #     headers = {'Authorization': self.token, 'Content-Type': 'application/json'}
    #     status = None
    #     i = 0
    #     async with aiohttp.ClientSession() as session:
    #         while (status != 'done') and i < 40:
    #             async with session.get(url, headers=headers) as response:
    #                 if response.status == 200:
    #                     data = await response.json()
    #                     status = data.get("data").get('status')
    #                     print(f'status = {status}')
    #                 else: print(f"check_status:{response.status} {await response.json()}")
    #                 await asyncio.sleep(3)
    #                 i +=1
    #         if status == 'done': return True
    #         else: return False

    # async def get_stocks(self, taskId):
    #     url = f"{base_url}/api/v1/warehouse_remains/tasks/{taskId}/download"
    #     headers = {'Authorization': self.token, 'Content-Type': 'application/json'}
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get(url, headers=headers) as response:
    #             if response.status == 200:
    #                 data = await response.json()
    #                 return data
    #         return None
    async def get_stock(self, wb_token: str):
        date = (datetime.now()).strftime('%Y-%m-%d')
        headers = {'Authorization': wb_token}

        json_data = []
        lastChangeDate = date
        data = ["data"]
        while data != []:
            url = f'https://statistics-api.wildberries.ru/api/v1/supplier/stocks?dateFrom={lastChangeDate}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url, headers=headers) as response:
                    data = await response.json()
                    if response.status == 200:
                        for row in data:
                            lastChangeDate = row["lastChangeDate"]
                            nmId = row["nmId"]
                            quantityFull = row["quantityFull"]
                            json_data.append({"nmId": nmId, "quantityFull": quantityFull, 'subject':row['subject']})
                        if len(data)>=60000:
                            await asyncio.sleep(60)
                        else:
                            break
                    else:
                        logging.error("Stocks data was not obtain fully. Status {status}".format(status=response.status))
                        break
        return json_data

    async def write_to_file(self, data):
        with open(f"data/{self.bot_username}_stocks.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return None
    
    # def get_from_file(self):
    #     with open(f"{self.bot_username}_stocks.json", 'r', encoding='utf-8') as f:
    #         data = json.load(f)
    #         return data
    #     return None
    
    # def get_list_of_products(self, data):
    #     list_of_products = []
    #     for i in range(len(data)):
    #         if data[i]["quantityWarehousesFull"] > 0:
    #             list_of_products.append(f'{data[i]["subjectName"]} Арт. {data[i]["nmId"]}')
        
    #     prod = ", ".join(list_of_products)
    #     return prod
    async def get_wb_token_loop(self):
        while True:    
            self.token = (await get_one_bot(bot_username=self.bot_username)).wb_token
            if not self.token or self.token == '':
                asyncio.sleep(60)
            else: return True
        return False

    async def run(self):
        while True:
            logging.info('STOCKS UPDATING...')
            await self.get_wb_token_loop()
            # self.token = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjUwMjE3djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTc1NjI1MDkyMiwiaWQiOiIwMTk1M2NkZC1jODllLTczNTQtYmUyNS04NzE0NzJlZmRhNDEiLCJpaWQiOjQ5NjE0OTU0LCJvaWQiOjIwNjMxMSwicyI6MTA3Mzc0OTc1OCwic2lkIjoiZGE4ZjBlNGYtMjQ3MC00MzFhLWI2MTEtMTA2YmJhYjMyYzM3IiwidCI6ZmFsc2UsInVpZCI6NDk2MTQ5NTR9.gESAyZPaSJZChRadpb7iMnWi9gr1UG73-vo_al55xJkEetqdARMBBHqUz9mvEkuDdwY7AfHoVjH80TKta5kl4Q'
            # taskId = await self.request_for_stocks()
            # print(taskId)
            # if await self.check_status(taskId):
            #     data = await self.get_stocks(taskId)
            #     print(data)
            #     data = self.extendtofull(data)
            #     await self.write_to_file(data)
            data = await self.get_stock(self.token) 
            if data:
                await self.write_to_file(data)
                print('\ndata obtained\n')
            else:
                logging.error(f'Stock data in bot {self.bot_username} was not obtained.')
                print('\ndata NOT obtained\n')
            await asyncio.sleep(self.interval * 60)    

def get_random_three_str( 
    bot_info,
    current_nmId :int = 0, 
    number_of_art :int = 3,
    samples_ans :list = ["Рекомендуем присмотреться к этим вариантам: ", "Также у нас есть и другие товары в наличии: ", "Посмотрите, что у нас есть ещё: ", "Также, возможно вас заинтересует: ", "Также у нас в наличии есть: ", "Смотрите, что у нас есть ещё: "]
    ):
    bot_username = bot_info.bot_username
    number_of_art = bot_info.number_of_art if bot_info.number_of_art is not None else number_of_art
    samples_ans = bot_info.samples_ans if bot_info.samples_ans else samples_ans
    
    try:
        with open(f"data/{bot_username}_stocks.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:data = {} 
    rand_data = []
    for i in range(min(number_of_art, len(data))):
        j = 7
        while j > 0 and len(data) > 0:
            j -= 1
            r = rand.randint(0, len(data)-1)
            if data[r]["quantityFull"] > 0 and data[r]["nmId"] != current_nmId:
                break
            else:
                continue
        if data[r]["quantityFull"] == 0 or data[r]["nmId"] == current_nmId:
            break
        rand_data.append(f'{data[r]["subject"]} Арт. {data[r]["nmId"]}')
        del data[r]
    random_three_str = samples_ans[rand.randint(0, len(samples_ans)-1)] if rand_data else ""
    random_three_str+=", ".join(rand_data)
    return random_three_str

async def main_wbstat():
    # wb = WBStat('testconnectwb_bot')
    # await wb.run()
    bot_info = await get_one_bot(bot_username='testconnectwb_bot')
    data = get_random_three_str(bot_info)
    print(f"data: ({data})")

'''
        
        Примеры ответа data от сервера

            Content type
            application/json

            Копировать
            Показать все
            [
            {
            "brand": "Wonderful",
            "subjectName": "Фотоальбомы",
            "vendorCode": "41058/прозрачный",
            "nmId": 183804172,
            "barcode": "2037031652319",
            "techSize": "0",
            "volume": 1.33,
            "inWayToClient": 31,
            "inWayFromClient": 24,
            "quantityWarehousesFull": 134,
            "warehouses": [
            {
            "warehouseName": "Невинномысск",
            "quantity": 134
            }
            ]
            }
            ]
        
        '''
if __name__ == '__main__':
    data =            [
            {
            "brand": "Wonderful",
            "subjectName": "Картинки",
            "vendorCode": "41058/прозрачный",
            "nmId": 183804172,
            "barcode": "2037031652319",
            "techSize": "0",
            "volume": 1.33,
            "inWayToClient": 31,
            "inWayFromClient": 24,
            "quantityWarehousesFull": 134,
            "warehouses": [
            {
            "warehouseName": "Невинномысск",
            "quantity": 134
            }
            ]
            },
                       {
            "brand": "Wonderful",
            "subjectName": "Колонки",
            "vendorCode": "41058/прозрачный",
            "nmId": 183804172,
            "barcode": "2037031652319",
            "techSize": "0",
            "volume": 1.33,
            "inWayToClient": 31,
            "inWayFromClient": 24,
            "quantityWarehousesFull": 134,
            "warehouses": [
            {
            "warehouseName": "Невинномысск",
            "quantity": 134
            }
            ]
            }, 
          {
            "brand": "Wonderful",
            "subjectName": "Нулевое количесвтво",
            "vendorCode": "41058/прозрачный",
            "nmId": 183804172,
            "barcode": "2037031652319",
            "techSize": "0",
            "volume": 1.33,
            "inWayToClient": 31,
            "inWayFromClient": 24,
            "quantityWarehousesFull": 0,
            "warehouses": [
            {
            "warehouseName": "Невинномысск",
            "quantity": 0
            }
            ]
            }
 ,           {
            "brand": "Wonderful",
            "subjectName": "Краски",
            "vendorCode": "41058/прозрачный",
            "nmId": 183804172,
            "barcode": "2037031652319",
            "techSize": "0",
            "volume": 1.33,
            "inWayToClient": 31,
            "inWayFromClient": 24,
            "quantityWarehousesFull": 134,
            "warehouses": [
            {
            "warehouseName": "Невинномысск",
            "quantity": 134
            }
            ]
            }
,
            {
            "brand": "Wonderful",
            "subjectName": "Наушники",
            "vendorCode": "41058/прозрачный",
            "nmId": 11112222,
            "barcode": "2037031652319",
            "techSize": "0",
            "volume": 1.33,
            "inWayToClient": 31,
            "inWayFromClient": 24,
            "quantityWarehousesFull": 134,
            "warehouses": [
            {
            "warehouseName": "Невинномысск",
            "quantity": 134
            }
            ]
            },
                       {
            "brand": "Wonderful",
            "subjectName": "Клавиатура",
            "vendorCode": "41058/прозрачный",
            "nmId": 4445555,
            "barcode": "2037031652319",
            "techSize": "0",
            "volume": 1.33,
            "inWayToClient": 31,
            "inWayFromClient": 24,
            "quantityWarehousesFull": 134,
            "warehouses": [
            {
            "warehouseName": "Невинномысск",
            "quantity": 134
            }
            ]
            }
 ,           {
            "brand": "Wonderful",
            "subjectName": "Компьютер",
            "vendorCode": "41058/прозрачный",
            "nmId": 77770000,
            "barcode": "2037031652319",
            "techSize": "0",
            "volume": 1.33,
            "inWayToClient": 31,
            "inWayFromClient": 24,
            "quantityWarehousesFull": 0,
            "warehouses": [
            {
            "warehouseName": "Невинномысск",
            "quantity": 0
            }
            ]
            }
 ,           {
            "brand": "Wonderful",
            "subjectName": "Мышь красная",
            "vendorCode": "41058/прозрачный",
            "nmId": 99998888,
            "barcode": "2037031652319",
            "techSize": "0",
            "volume": 1.33,
            "inWayToClient": 31,
            "inWayFromClient": 24,
            "quantityWarehousesFull": 134,
            "warehouses": [
            {
            "warehouseName": "Невинномысск",
            "quantity": 134
            }
            ]
            }
 
            ]
 
    # wb = WBStat("testconnectwb_bot")
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main_wbstat())