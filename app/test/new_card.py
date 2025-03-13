import asyncio
import aiohttp
from configparser import ConfigParser
import sys
sys.path.append(".")
from db.get import get_all_bots
import logging
from datetime import datetime, timedelta
import requests
source_link = "https://content-api-sandbox.wildberries.ru"
# source_link = "https://content-api.wildberries.ru"
async def new_cards(cards_list : list):
    infobots = await get_all_bots()
    wb_token = infobots[0].wb_token
    print("wb_token: "+ str(wb_token)+ "\n")
    headers = {'Authorization':wb_token}
    lnk = "/content/v2/cards/upload"
    async with aiohttp.ClientSession() as session:
        async with session.post(source_link+lnk,json=cards_list,headers=headers) as r:
            if r.status == 200:
                print("\n\n============SUCCESS=============\n\n")
            else: print('\n\nStatus code: '+str(r.status)+'\n\n')
            return await r.json()

async def object_query():
    link = "https://content-api-sandbox.wildberries.ru/content/v2/object/parent/all"
    # wb_token ="eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjUwMjE3djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTc1NjU3MTEzMCwiaWQiOiIwMTk1NGZmMy1jM2VlLTcyY2ItODEwNS01OGM4MTViMDcwMWMiLCJpaWQiOjg3MDEyMzgwLCJvaWQiOjQ0NjgxMjksInMiOjAsInNpZCI6IjExZmQwNDYxLWYxMjQtNGY1Ny04N2I0LWIyZTI5YThiNWNiNyIsInQiOnRydWUsInVpZCI6ODcwMTIzODB9.T88bCwprqeEaq-d87esMQzVv-YQ7NJ_OjUXWMlBnCkIEPWKBg6qjzQ6u1KFwFMNQI4n-2-_7JFZoSUKVsQT_rw"
    infobots = await get_all_bots()
    wb_token = infobots[0].wb_token
    headers = {'Authorization':wb_token}
    async with aiohttp.ClientSession() as session:
        async with session.get(link, headers=headers) as r:
            if r.status == 200:
                print("\n\n============SUCCESS=============\n\n")
            else: print('\n\nStatus code: '+str(r.status)+'\n\n')
            return await r.json()

async def Get():
    link = 'https://content-api-sandbox.wildberries.ru/content/v2/object/all?name=Носки'
    # wb_token ="eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjUwMjE3djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTc1NjU3MTEzMCwiaWQiOiIwMTk1NGZmMy1jM2VlLTcyY2ItODEwNS01OGM4MTViMDcwMWMiLCJpaWQiOjg3MDEyMzgwLCJvaWQiOjQ0NjgxMjksInMiOjAsInNpZCI6IjExZmQwNDYxLWYxMjQtNGY1Ny04N2I0LWIyZTI5YThiNWNiNyIsInQiOnRydWUsInVpZCI6ODcwMTIzODB9.T88bCwprqeEaq-d87esMQzVv-YQ7NJ_OjUXWMlBnCkIEPWKBg6qjzQ6u1KFwFMNQI4n-2-_7JFZoSUKVsQT_rw"
    infobots = await get_all_bots()
    wb_token = infobots[0].wb_token
    headers = {'Authorization':wb_token}
    # body =    {
    #       "settings": {                      
    #         "cursor": {
    #           "limit": 100
    #         },
    #         "filter": {
    #           "withPhoto": -1
    #         }
    #       }
    #     }
    # body = {"name":"свечи", "parentID": 195}
    async with aiohttp.ClientSession() as session:
        async with session.get(link, headers=headers) as r:
            if r.status == 200:
                print("\n\n============SUCCESS=============\n\n")
            else: print('\n\nStatus code: '+str(r.status)+'\n\n')
            return await r.json()

async def object_query():
    link = "https://content-api-sandbox.wildberries.ru/content/v2/get/cards/list"
    # wb_token ="eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjUwMjE3djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTc1NjU3MTEzMCwiaWQiOiIwMTk1NGZmMy1jM2VlLTcyY2ItODEwNS01OGM4MTViMDcwMWMiLCJpaWQiOjg3MDEyMzgwLCJvaWQiOjQ0NjgxMjksInMiOjAsInNpZCI6IjExZmQwNDYxLWYxMjQtNGY1Ny04N2I0LWIyZTI5YThiNWNiNyIsInQiOnRydWUsInVpZCI6ODcwMTIzODB9.T88bCwprqeEaq-d87esMQzVv-YQ7NJ_OjUXWMlBnCkIEPWKBg6qjzQ6u1KFwFMNQI4n-2-_7JFZoSUKVsQT_rw"
    infobots = await get_all_bots()
    wb_token = infobots[0].wb_token
    headers = {'Authorization':wb_token}
    # body =    {
    #       "settings": {                      
    #         "cursor": {
    #           "limit": 100
    #         },
    #         "filter": {
    #           "withPhoto": -1
    #         }
    #       }
    #     }
    # body = {"name":"свечи"}
    body = {}
    async with aiohttp.ClientSession() as session:
        async with session.post(link, headers=headers, json=body) as r:
            if r.status == 200:
                print("\n\n============SUCCESS=============\n\n")
            else: print('\n\nStatus code: '+str(r.status)+'\n\n')
            return await r.json()
        
async def get_feedbacks():
    domain = "https://feedbacks-api-sandbox.wildberries.ru"
    link = domain + "/api/v1/feedbacks/count"
    # link+="?isAnswered=true&take=20&skip=0"
    infobots = await get_all_bots()
    wb_token = infobots[0].wb_token
    headers = {'Authorization':wb_token}
    async with aiohttp.ClientSession() as session:
        async with session.get(link, headers=headers) as r:
            if r.status == 200:
                print("\n\n============SUCCESS=============\n\n")
            else: print('\n\nStatus code: '+str(r.status)+'\n\n')
            return await r.json()


async def get_feedback_data(time_now: datetime = datetime.now()):
    wb_feedbacks_link = 'https://feedbacks-api-sandbox.wildberries.ru'

    infobots = await get_all_bots()
    wb_token = infobots[0].wb_token

    url = f"{wb_feedbacks_link}/api/v1/feedbacks?isAnswered=false&take=5&skip=0"
    header = {"Authorization": wb_token}
    with requests.get(url, headers=header) as response:
        response.encoding = "utf-8"
        # last_munutes = time_now - timedelta(minutes=self.interval, hours=3, days=3)
        if response.status_code == 200:
            data = response.json()
            return data
            feedback_list = []
            i = 0
            # while i < len(
            #     data["data"]["feedbacks"]
            # ):  # i < data['data']['countUnanswered']
            #     feedback_date = data["data"]["feedbacks"][i]["createdDate"]
            #     feedback_text = data["data"]["feedbacks"][i]["text"]
            #     feedback_pros = data["data"]["feedbacks"][i]["pros"]
            #     feedback_cons = data["data"]["feedbacks"][i]["cons"]
            #     fb_video = data["data"]["feedbacks"][i]["video"]
            #     fb_photoLinks = data["data"]["feedbacks"][i]["photoLinks"]
            #     # if (
            #     #     datetime.strptime(feedback_date, "%Y-%m-%dT%H:%M:%SZ")
            #     #     > last_munutes
            #     # ):
            #     feedback_id = data["data"]["feedbacks"][i]["id"]
            #     feedback_valuation = data["data"]["feedbacks"][i][
            #         "productValuation"
            #     ]
            #     product_nmId = data["data"]["feedbacks"][i]["productDetails"][
            #         "nmId"
            #     ]
            #     product_name = data["data"]["feedbacks"][i]["productDetails"][
            #         "productName"
            #     ]
            #     username = data["data"]["feedbacks"][i]["userName"]
            #     feedback_list.append(
            #         {
            #             "id": feedback_id,
            #             "text": feedback_text,
            #             "pros": feedback_pros,
            #             "cons": feedback_cons,
            #             "valuation": feedback_valuation,
            #             "date": feedback_date,
            #             "product_nmId": product_nmId,
            #             "product_name": product_name,
            #             "username": username,
            #         }
            #     )
            #     i += 1
            # print('------------------------==========================-----------------',feedback_list)
            # return feedback_list
        else:
            logging.error(f"Error: {response.status_code}")
            data = response.json()

            return data["errorText"]


if __name__=="__main__":
    card_list = [{"subjectID":744, "variants":[{"brand":"SSet WrmStone","title": "Candles - Свечи","description": "Свечи гладкие круглые","vendorCode":"cnd0001", "sizes":[{"price": 3000,"skus": ["sku333333"]}], "characteristics":[{"id":3, "value":"vax"}, {"id":4, "value":"paraphine"}]}]},
                 {"subjectID":744, "variants":[{"brand":"SSet Craft","title": "Свечи","description": "Свечи маленькие круглые","vendorCode":"cnd-crt-0001", "sizes":[{"price": 200,"skus": ["sku001111"]}], "characteristics":[{"id":1, "value":"vax"}, {"id":2, "value":"paraphine"}]}]}
                 ]
    # data = asyncio.run(new_cards(card_list))
    data = asyncio.run(object_query())
    # data = asyncio.run(Get())
    # data = asyncio.run(get_feedback_data())
    print(data)