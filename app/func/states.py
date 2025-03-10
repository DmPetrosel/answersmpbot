from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    first_name = State()
    username = State()
    promocode = State()
    description = State()
    company_name = State()

class NewPromo(StatesGroup):
    promo_name_state = State()
    expiering_date_state = State()
    price_state = State()

class NewBot(StatesGroup):
    get_bot_token = State()
    get_wb_token = State()

class FeedState(StatesGroup):
    mess_answering = State()
class PayState(StatesGroup):
    enter_sum = State()
    successful_payment = State()
    buying = State()
    precheckout = State()
