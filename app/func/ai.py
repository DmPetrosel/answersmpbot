from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from configparser import ConfigParser
from wbstat import *
config = ConfigParser()
config.read('config.ini', encoding='utf-8')
access_token = config.get('gigachat','access_token')
def generate_answer_for_feedback_ai(company, company_description, feedback):
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

    # Используйте токен, полученный в личном кабинете из поля Авторизационные данные
    with GigaChat(credentials=access_token,
    scope='GIGACHAT_API_CORP',
    model='GigaChat', 
    verify_ssl_certs=False) as giga:
        user_input = feedback
        payload.messages.append(Messages(role=MessagesRole.USER, content=user_input))
        response = giga.chat(payload)
        # payload.messages.append(response.choices[0].message)
        return  response.choices[0].message.content
    
def generate_answer(company, company_description, feedback, bot_info):
    str_answer = generate_answer_for_feedback_ai(company, company_description, feedback)
    str_answer = str_answer + "\n" + get_random_three_str(bot_info)
    return str_answer
if __name__ == '__main__':
    company = input("Введите название компании: ")
    company_description = input("Введите описание компании: ")
    # articuls = input("Введите список артикулов: ")
    articuls = "Краски - Арт 183804171, Колонки - Арт 183804172, Картинки - Арт 183804173, Клавиатура - Арт 111804171, Мышь - Арт 112804172, Наушники - Арт 113804173"
    while True:
        feedback = input("Введите отзыв: ")
        print(generate_answer_for_feedback_ai(company, company_description, feedback))