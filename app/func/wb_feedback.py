import json
import requests
from datetime import datetime, timedelta
import time
from threading import Thread
import logging
import asyncio

# import handle_errors
import random as rd
from db.get import *
from db.set import *
from db.update import *
import aiohttp

# handle_errors.logger_params()
# with open("data/config.json", "r", encoding="UTF-8") as config_file:
#     config = json.load(config_file)
#     # gs_rnp_key = config["gs_rnp_key_wb"]
#     wb_token = config["token_wb"]
#     gs_feed_key = config["gs_feed_key"]
# credentials = ServiceAccountCredentials.from_json_keyfile_name(
#     # filename='data/pythonwb-399809-39ae2efa6d1f.json',
#     filename='data/speedy-elf-429605-i4-315d54804473.json',
#     scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

# gc = gspread.authorize(credentials)


class WBFeedback(Thread):
    def __init__(self, wb_token, bot_username, bot, interval=15, quantity_of_cards=100):
        super().__init__()
        self.daemon = False
        self.interval = interval
        self.quantity_of_cards = quantity_of_cards
        self.wb_token = wb_token
        self.bot_username = bot_username
        self.bot = bot

    def get_feedback_wb(self, wb_token, time_now: datetime):
        url = f"https://feedbacks-api.wildberries.ru/api/v1/feedbacks?isAnswered=false&take={self.quantity_of_cards}&skip=0"
        header = {"Authorization": self.wb_token}
        with requests.get(url, headers=header) as response:
            response.encoding = "utf-8"
            last_munutes = time_now - timedelta(minutes=self.interval, hours=3, days=3)
            if response.status_code == 200:
                data = response.json()
                feedback_list = []
                i = 0
                while i < len(
                    data["data"]["feedbacks"]
                ):  # i < data['data']['countUnanswered']
                    feedback_date = data["data"]["feedbacks"][i]["createdDate"]
                    feedback_text = data["data"]["feedbacks"][i]["text"]
                    feedback_pros = data["data"]["feedbacks"][i]["pros"]
                    feedback_cons = data["data"]["feedbacks"][i]["cons"]
                    fb_video = data["data"]["feedbacks"][i]["video"]
                    fb_photoLinks = data["data"]["feedbacks"][i]["photoLinks"]
                    if (
                        datetime.strptime(feedback_date, "%Y-%m-%dT%H:%M:%SZ")
                        > last_munutes
                    ):
                        feedback_id = data["data"]["feedbacks"][i]["id"]
                        feedback_valuation = data["data"]["feedbacks"][i][
                            "productValuation"
                        ]
                        product_nmId = data["data"]["feedbacks"][i]["productDetails"][
                            "nmId"
                        ]
                        product_name = data["data"]["feedbacks"][i]["productDetails"][
                            "productName"
                        ]
                        username = data["data"]["feedbacks"][i]["userName"]
                        feedback_list.append(
                            {
                                "id": feedback_id,
                                "text": feedback_text,
                                "pros": feedback_pros,
                                "cons": feedback_cons,
                                "valuation": feedback_valuation,
                                "date": feedback_date,
                                "product_nmId": product_nmId,
                                "product_name": product_name,
                                "username": username,
                            }
                        )
                    i += 1
                # print(feedback_list)
                return feedback_list
            else:
                logging.error(f"Error: {response.status_code}")
                data = response.json()

                return data["errorText"]

    def write_to_db(self, feedbacks_list):
        fb_db_feedids = asyncio.run(
            [fb.feed_id for fb in get_all_wbfeed(bot_username=self.bot_username)]
        )
        for fb in feedbacks_list:
            if fb["id"] not in fb_db_feedids:
                text = fb["text"] + "\n\n" if fb["text"] else ""
                pros = str("Плюсы: " + fb["pros"] + "\n\n") if fb["pros"] else ""
                cons = str("Минусы: " + fb["cons"] + "\n\n") if fb["cons"] else ""
                mess = str(text + pros + cons)
                valuation = fb["valuation"]
                material_links = str(fb["photoLinks"] + "\n\n" + fb["video"])
                createdDate = datetime.strptime(
                    fb["createdDate"], "%Y-%m-%dT%H:%M:%SZ"
                ) + timedelta(hours=3)

                asyncio.run(add_wbfeed(
                    feed_id=fb["id"],
                    valuation=valuation,
                    material_links=material_links,
                    bot_username=self.bot_username,
                    feed_mess=mess,
                    createdDate=createdDate,
                    time_now=datetime.now(),
                    material_links=material_links
                )
                )

    # def new_feedbacks_to_file(self, time_now: datetime):
    #     old_feedbacks = []
    #     try:
    #         with open(
    #             "data/old_feedbacks_wb.json", "r", encoding="UTF-8"
    #         ) as old_feed_file:
    #             old_feedbacks = json.load(old_feed_file)
    #     except:
    #         pass
    #     feedbacks_wb = self.get_feedback_wb(self.wb_token, time_now)
    #     res = []
    #     for fb in feedbacks_wb:
    #         if fb not in old_feedbacks:
    #             res.append(fb)
    #     with open("data/old_feedbacks_wb.json", "w", encoding="UTF-8") as old_feed_file:
    #         json.dump(feedbacks_wb, old_feed_file, ensure_ascii=False, indent=4)

    #     with open(
    #         "data/new_feedbacks_wb.json", "w", encoding="UTF-8"
    #     ) as new_messages_file:
    #         json.dump(res, new_messages_file, ensure_ascii=False, indent=4)
    #     return feedbacks_wb

    def run(self):
        logging.info("update feedback wb")
        self.new_feedbacks_to_file(datetime.now())


async def answer_for_feedback(feedback_id, text, wb_token):
    url = "https://feedbacks-api.wildberries.ru/api/v1/feedbacks/answer"
    header = {"Authorization": wb_token}
    body = {"id": feedback_id, "text": text}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=header, json=body) as response:
            if response.status == 204:
                logging.info(f"feedback {feedback_id} was answered with text: {text}")
                return True
            else:
                logging.error(
                    f"Error answer feedback {feedback_id} with status: {response.status}"
                )
                return False
    return


if __name__ == "__main__":
    # wb_feedback = WBFeedback()
    # wb_feedback.new_feedbacks_to_file(time_now=datetime.now())
    # wb_stocks = WBStocks()
    # wb_stocks.update_stocks(wb_token)
    # print(random_answer_text(128122716))
    # print(check_product_sells(215225682))
    pass