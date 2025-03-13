import aiohttp
import asyncio
import json
import requests
import time
import logging
from  threading import Thread
import random as rand
class WBStat:
    def __init__(self, wb_token, bot_username, 
                  daemon = True):
        self.token = wb_token
        self.bot_username = bot_username
        self.daemon = daemon
        self.interval = 30
    def request_for_stocks(self):
        url = "https://seller-analytics-api.wildberries.ru/api/v1/warehouse_remains"
        headers = {'Authorization': self.token, 'Content-Type': 'application/json'}
        with requests.get(url, headers=headers) as response:
            response.encoding = 'utf-8'
            data = response.json()
            taskId = data.get("data", 'taskId')
        return None

    def check_status(self, taskId):
        url = f"https://seller-analytics-api.wildberries.ru/api/v1/warehouse_remains/tasks/{taskId}/status"
        headers = {'Authorization': self.token, 'Content-Type': 'application/json'}
        status = None
        i = 0
        while (status == 'new' or status == 'processing')and i < 40:
            with requests.get(url, headers=headers) as response:
                response.encoding = 'utf-8'
                data = response.json()
                status = data.get("data", 'status')
                time.sleep(3)
                i +=1
        if status == 'done': return True
        else: return False

    def get_stocks(self, taskId):
        url = f"https://seller-analytics-api.wildberries.ru/api/v1/warehouse_remains/tasks/{taskId}/download"
        headers = {'Authorization': self.token, 'Content-Type': 'application/json'}
        with requests.get(url, headers=headers) as response:
            response.encoding = 'utf-8'
            data = response.json()
            return data
        return None

    def write_to_file(self, data):
        with open(f"{self.bot_username}_stocks.json", 'w', encoding='utf-8') as f:
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
        

    async def run(self):
        taskId = self.request_for_stocks()
        while True:
            logging.info('STOCKS UPDATING...')
            if self.check_status(taskId):
                data = self.get_stocks(taskId)
                self.write_to_file(data)
            else:
                logging.error(f'Stock data in bot {self.bot_username} was not obtained.')
            await asyncio.sleep(self.interval * 60)    

def get_random_three_str( 
    bot_info,
    number_of_art :int = 3,
    samples_ans :list = ["Рекомендуем присмотреться к этим вариантам: ", "Также у нас есть и другие товары в наличии: ", "Посмотрите, что у нас есть ещё: ", "Также, возможно вас заинтересует: ", "Также у нас в наличие есть: ", "Смотрите, что у нас есть ещё: "]
    ):
    bot_username = bot_info.bot_username
    number_of_art = bot_info.number_of_art if bot_info.number_of_art != 0 else number_of_art
    samples_ans = bot_info.samples_ans if bot_info.samples_ans else samples_ans
    
    with open(f"data/{bot_username}_stocks.json", 'r', encoding='utf-8') as f:
        data = json.load(f)

    rand_data = []
    for i in range(min(number_of_art, len(data))):
        j = 7
        while j > 0 and len(data) > 0:
            j -= 1
            r = rand.randint(0, len(data)-1)
            if data[r]["quantityWarehousesFull"] > 0:
                break
            else:
                continue
        if data[r]["quantityWarehousesFull"] == 0:
            break
        rand_data.append(f'{data[r]["subjectName"]} Арт. {data[r]["nmID"]}')
        del data[r]
    random_three_str = samples_ans[rand.randint(0, len(samples_ans)-1)]
    random_three_str+=", ".join(rand_data)
    return random_three_str

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
 
    wb = WBStat("dafsadfs", "booooooooot_bot", daemon=False)
    r3 = wb.get_random_three_str(data)
    print(r3)