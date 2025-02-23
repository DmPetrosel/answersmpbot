from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from configparser import ConfigParser
from wbstat import *
from db.update import *
from db.get import get_one_bot
import logging
config = ConfigParser()
config.read('config.ini', encoding='utf-8')
access_token = config.get('gigachat','access_token')
ratio = int(config.get('gigachat','ratio'))
async def generate_answer_for_feedback_ai(feedback, bot_info):
    company=bot_info.company_name
    company_description=bot_info.company_description
    balance = bot_info.user.balance
    user_id = bot_info.user.id
    payload = Chat(
        messages=[
            Messages(
                role=MessagesRole.SYSTEM,
                content="Ты хороший в внимательный продавец в компании" + company + ", с таким описанием: " + company_description +"\nНапиши вежливый ответ на отзыв покупателя в итернете."
            )
        ],
        temperature=0,
        max_tokens=100,
    )
    content = ""
    # Используйте токен, полученный в личном кабинете из поля Авторизационные данные
    with GigaChat(credentials=access_token,
    scope='GIGACHAT_API_CORP',
    model='GigaChat', 
    verify_ssl_certs=False) as giga:
        user_input = feedback
        payload.messages.append(Messages(role=MessagesRole.USER, content=user_input))
        response = giga.chat(payload)
        # payload.messages.append(response.choices[0].message)
        total_tokens = int(response.usage.total_tokens)
        user_cost = total_tokens*2/10000*ratio
        logging.info(f"{bot_info.bot_username} use {total_tokens} wich cost {total_tokens*2/10000} for user it cost {user_cost} as feedback")
        content=   response.choices[0].message.content
    await update_user_by_id(id=user_id, balance=balance-user_cost)
    return content
async def generate_answer(feedback, bot_info):
    str_answer = await generate_answer_for_feedback_ai(feedback, bot_info)
    str_answer = str_answer + "\n" + get_random_three_str(bot_info)
    return str_answer

async def ai_main():
    bot_info = await get_one_bot(bot_username="testconnectwb_bot")
    # company = input("Введите название компании: ")
    # company_description = input("Введите описание компании: ")
    # articuls = input("Введите список артикулов: ")
    articuls = "Краски - Арт 183804171, Колонки - Арт 183804172, Картинки - Арт 183804173, Клавиатура - Арт 111804171, Мышь - Арт 112804172, Наушники - Арт 113804173"
    while True:
        feedback = input("Введите отзыв: ")
        answer = await generate_answer_for_feedback_ai(feedback, bot_info)
        print(answer)
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', encoding='utf-8', filemode='a', filename='data/log.log')

    asyncio.run(ai_main())