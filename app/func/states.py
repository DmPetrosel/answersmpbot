from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    first_name = State()
    username = State()
    promocode = State()

class NewPromo(StatesGroup):
    promo_name_state = State()
    expiering_date_state = State()
    price_state = State()