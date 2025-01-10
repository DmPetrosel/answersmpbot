from create_bot import *
from aiogram.fsm.context import FSMContext
from db.get import *
from keyboard.marketer_kb import *
import aiogram
user_obj = {}
async def marketer(chat_id: int):
    '''Маркетолог должен быть самозанятым и оформлять получение средств как продажа.
    У марктолога будет в главном меню:
        - текущий баланс. 
    Он сможет делать все действия с промокодами:
        а)посмотреть промокоды, 
        б)создавать промокоды с той ценой, которой он посчитает нужной, комиссию он получит 10%,
        в)удалять промокоды. 
    
    Для промокода можно будет 
        1.устанавливать цену, но не менее 30 к, 
        2.устанавливать конечную дату, 
        3.будет создана реферальная ссылка на промокод
    '''
    user_obj[chat_id] = await get_user(chat_id)
    balance = user_obj[chat_id].balance
    await bot.send_message(chat_id,  f"Ваш баланс: {balance}", reply_markup=marketer_menu_kb())

async def callback_marketer(call: types.CallbackQuery):
    # await call.answer(cache_time=60)
    print('callback marketer')
    if call.data == 'my_promos':
        promos_list = await get_all_promos(call.from_user.id)
        # dictionry = [[i.promocode, i.price, i.expire_date, i.User.username] for i in promos_list]
        print(promos_list)
        # await call.message.edit_text(f"Ваш баланс: {balance}", reply_markup=marketer_menu_kb)
    # elif call.data == 'create_promo':
    #     promocodes = await get_promocodes(call.from_user.id)
    #     if promocodes:
    #         await call.message.edit_text(f"Ваши промокоды: \n{promocodes}", reply_markup=marketer_menu_kb)


dp.callback_query.register(callback_marketer, lambda c: c.data in ('my_promos', 'create_promo'))