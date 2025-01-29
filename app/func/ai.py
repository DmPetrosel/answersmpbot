from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from configparser import ConfigParser
config = ConfigParser()
config.read('app/config.ini', encoding='utf-8')
access_token = config['gigachat']['access_token']
def generate_answer_for_feedback(company, company_description, articuls, feedback):
    payload = Chat(
        messages=[
            Messages(
                role=MessagesRole.SYSTEM,
                content="Ты хороший в внимательный продавец в компании" + company + ", с таким описанием: " + company_description + ". Также, иногда ты предлагаешь приобрести дополнительные товары, которая предлагает компания из этого списка артикулов (не больше трёх и если у артикула нет наименования, даже если ты знаешь, чем компания занимается, пишешь просто предложение обратить внимание на артикул и его номер без привязки к товару. Например, также предлагаю обратить на товары с арт. и номер артикула): "+ articuls,
            )
        ],
        temperature=0.7,
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
        print("Bot: ", response.choices[0].message.content, "\n\n")


company = input("Введите название компании: ")
company_description = input("Введите описание компании: ")
articuls = input("Введите список артикулов: ")
while True:
    feedback = input("Введите отзыв: ")
    generate_answer_for_feedback(company, company_description, articuls, feedback)