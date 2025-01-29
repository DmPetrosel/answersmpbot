import aiohttp
import asyncio
import json
import requests
import time
import logging
from  threading import Thread

class WBStat(Thread):
    def __init__(self, wb_token, bot_username, daemon = True):
        self.token = wb_token
        self.bot_username = bot_username
        self.daemon = daemon

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

    def run(self):
        taskId = self.request_for_stocks()
        if self.check_status(taskId):
            data = self.get_stocks(taskId)
            self.write_to_file(data)
        else:
            logging.error(f'Stock data in bot {self.bot_username} was not obtained.')
        return None
        