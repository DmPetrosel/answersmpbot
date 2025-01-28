import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import requests
from datetime import datetime, timedelta
import time
from threading import Thread
import logging
import handle_errors
import random as rd
handle_errors.logger_params()
with open("data/config.json", "r", encoding="UTF-8") as config_file:
    config = json.load(config_file)
    # gs_rnp_key = config["gs_rnp_key_wb"]
    wb_token = config["token_wb"]
    gs_feed_key = config["gs_feed_key"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    # filename='data/pythonwb-399809-39ae2efa6d1f.json',
    filename='data/speedy-elf-429605-i4-315d54804473.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

gc = gspread.authorize(credentials)

class WBFeedback(Thread):
    def __init__(self, interval = 15, quantity_of_cards = 100):
        super().__init__()
        self.daemon = False
        self.interval = interval
        self.quantity_of_cards = quantity_of_cards
    def get_feedback_wb(self, wb_token, time_now:datetime):
            url = f'https://feedbacks-api.wildberries.ru/api/v1/feedbacks?isAnswered=false&take={self.quantity_of_cards}&skip=0'
            header = {'Authorization': wb_token}
            with requests.get(url, headers=header) as response:
                response.encoding= 'utf-8'
                last_munutes = time_now - timedelta(minutes=self.interval, hours=3, days=3)
                if response.status_code== 200:
                    data = response.json()
                    feedback_list =[]
                    i = 0
                    while i < len(data['data']['feedbacks']): # i < data['data']['countUnanswered']
                        feedback_date = data['data']['feedbacks'][i]['createdDate']
                        feedback_text = data['data']['feedbacks'][i]['text']
                        feedback_pros = data['data']['feedbacks'][i]['pros']
                        feedback_cons = data['data']['feedbacks'][i]['cons']
                        fb_video = data['data']['feedbacks'][i]['video']
                        fb_photoLinks = data['data']['feedbacks'][i]['photoLinks']
                        if (datetime.strptime(feedback_date, "%Y-%m-%dT%H:%M:%SZ") > last_munutes) and (feedback_cons or feedback_pros or feedback_text or fb_video or fb_photoLinks):
                            feedback_id = data['data']['feedbacks'][i]['id']
                            feedback_valuation = data['data']['feedbacks'][i]['productValuation']
                            product_nmId = data['data']['feedbacks'][i]['productDetails']['nmId']
                            product_name = data['data']['feedbacks'][i]['productDetails']['productName']
                            username = data['data']['feedbacks'][i]['userName']
                            feedback_list.append({'id': feedback_id, 'text': feedback_text, 'pros':feedback_pros, 'cons':feedback_cons, 'valuation': feedback_valuation, 'date': feedback_date, 'product_nmId': product_nmId, 'product_name': product_name, 'username': username})
                        i+=1
                    # print(feedback_list)
                    return feedback_list
                else:
                    logging.error(f"Error: {response.status_code}")
                    data = response.json()

                    return data['errorText'] 
            
    def new_feedbacks_to_file(self, time_now:datetime):
        old_feedbacks = []
        try:
            with open('data/old_feedbacks_wb.json', 'r', encoding="UTF-8") as old_feed_file:
                old_feedbacks = json.load(old_feed_file)
        except:
            pass
        feedbacks_wb = self.get_feedback_wb(wb_token, time_now)
        res = []
        for fb in feedbacks_wb:
            if fb not in old_feedbacks:
                res.append(fb)
        with open('data/old_feedbacks_wb.json', 'w', encoding="UTF-8") as old_feed_file:
            json.dump(feedbacks_wb, old_feed_file, ensure_ascii=False, indent=4)
        
        with open('data/new_feedbacks_wb.json', 'w', encoding="UTF-8") as new_messages_file: 
            json.dump(res, new_messages_file, ensure_ascii=False, indent=4)
        return feedbacks_wb

    def run(self):
        logging.info('update feedback wb')
        self.new_feedbacks_to_file(datetime.now())

class WBStocks(Thread):
    def __init__(self, interval = 30):
        super().__init__()
        self.daemon = False
        self.interval = interval
    def get_stocks_wb(self, wb_token):
            # This request is one time a minute allowed.
            url= 'https://statistics-api.wildberries.ru/api/v1/supplier/stocks?dateFrom=2019-06-20T23:59:59'
            header = {'Authorization': wb_token}
            with requests.get(url, headers=header) as response:
                response.encoding= 'utf-8'
                if response.status_code== 200:
                    data = response.json()
                    stocks_list =[]
                    for stock in data:
                        stocks_list.append({"nmId":stock["nmId"], "quantity":stock["quantity"]})
                    # print(feedback_list)
                    return stocks_list
                else:
                    logging.error(f"Error: {response.status_code}")
                    return []    
    def update_stocks(self, wb_token):
        res = self.get_stocks_wb(wb_token)
        if res:
            with open('data/stocks_wb.json', 'w', encoding="UTF-8") as stocks_file: 
                json.dump(res, stocks_file, ensure_ascii=False, indent=4)

    def run(self):
        logging.info('start scheduler wb stocks')
        while True:
            if datetime.now().minute % self.interval == 0:
                logging.info('update stocks wb')
                self.update_stocks(wb_token=wb_token)
                # print(new_messages, '\n\ntotal unanswered messages:', total_unread_messages)
                time.sleep(60)
            else:
                time.sleep(60)


def answer_for_feedback_obsolete(feedback_id, text):
    url = 'https://feedbacks-api.wildberries.ru/api/v1/feedbacks'
    header = {'Authorization': wb_token}
    body = {'id': feedback_id, 'text': text}
    with requests.patch(url, headers=header, json=body) as response:
        if response.status_code == 200:
            logging.info(f'feedback {feedback_id} was answered with text: {text}')
        else:
            logging.error(f"Error answer feedback {feedback_id} with status: {response.status_code}")


def answer_for_feedback(feedback_id, text):
    url = 'https://feedbacks-api.wildberries.ru/api/v1/feedbacks/answer'
    header = {'Authorization': wb_token}
    body = {'id': feedback_id, 'text': text}
    with requests.post(url, headers=header, json=body) as response:
        if response.status_code == 204:
            logging.info(f'feedback {feedback_id} was answered with text: {text}')
        else:
            logging.error(f"Error answer feedback {feedback_id} with status: {response.status_code}")


def c_len(row):
    i = 0
    while i < len(row) and row[i]!=None:
        i+=1
    return i

def check_product_sells(nmId):
    status = False
    stocks = []
    try:
        with open('data/stocks_wb.json', 'r', encoding="UTF-8") as stocks_file:
            stocks = json.load(stocks_file)
    except:
        logging.error("Error load stocks")
    for stock in stocks:
        if stock['nmId'] == nmId:
            if stock['quantity'] > 0:
                status = True
            break
    return status
def get_all_nmIds():
    try:
        with open('data/stocks_wb.json', 'r', encoding="UTF-8") as stocks_file:
            stocks = json.load(stocks_file)
    except:
        logging.error("Error load stocks get_all_nmIds")
    nmIds = []
    for stock in stocks:
        nmIds.append(stock['nmId'])
    return nmIds
    

def random_answer_text(articul):
    # data = pd.read_excel('data/feedback_answers.xlsx', sheet_name='WB')
    # df = pd.DataFrame(data)
    # json_data =df.to_json(orient='values', force_ascii=False)
    table = gc.open_by_key(gs_feed_key)
    worksheet = table.worksheet("WB")
    parsed_json = worksheet.get_all_values()
    # print(parsed_json)
    # parsed_json = json.loads(json_data)
    answer_text = ''
    is_all_ok = False
    nmIds = get_all_nmIds()
    for i in parsed_json:
        # print(i)
        if str(i[1]) == str(articul):
            count_try = 0
            is_all_ok = False
            while count_try < 5 and not is_all_ok:
                count_try+=1
                num = rd.randint(2, c_len(i)-1)
                # return i[num]
                answer_text = i[num]
                is_all_ok = False
                for nmId in nmIds:
                    if str(nmId) in answer_text:
                        if check_product_sells(nmId):
                            is_all_ok = True
                        else:
                            is_all_ok = False
                            break
            break
    # time.sleep(2)
    if is_all_ok: return answer_text
    return "Здравствуйте! Нам очень приятно, что наша продукция стала полезной для Вас. Ваш положительный опыт работы с нашей продукцией вдохновляет нас на дальнейший рост и развитие. Будем рады видеть Вас и дальше в числе наших постоянных клиентов. С наилучшими пожеланиями, команда Collart."

if __name__== '__main__':
    # wb_feedback = WBFeedback()
    # wb_feedback.new_feedbacks_to_file(time_now=datetime.now())
    # wb_stocks = WBStocks()
    # wb_stocks.update_stocks(wb_token)
    print(random_answer_text(128122716))
    # print(check_product_sells(215225682))