from create_bot import *
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.filters import StateFilter
from db.get import *
from keyboard.marketer_kb import *
import aiogram
from func.states import *
from datetime import datetime, timedelta
from db.set import *
import configparser
user_obj = {}
promos_dict = {}
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

async def callback_marketer(call: types.CallbackQuery, state: FSMContext):
    # await call.answer(cache_time=60)
    print('callback marketer')
    if call.data == 'my_promos':
        promos_list = await get_all_promos(call.from_user.id)
        # dictionry = [[i.promocode, i.price, i.expire_date, i.User.username] for i in promos_list]
        print(promos_list)
        # await call.message.edit_text(f"Ваш баланс: {balance}", reply_markup=marketer_menu_kb)
    elif call.data == 'create_promo':
        promos_dict[call.from_user.id] = {}
        await call.message.edit_text('Введите промокод')
        await state.set_state('promo_name_state')
    #     promocodes = await get_promocodes(call.from_user.id)
    #     if promocodes:
    #         await call.message.edit_text(f"Ваши промокоды: \n{promocodes}", reply_markup=marketer_menu_kb)

async def new_promo(message:types.Message, state: FSMContext):
    var = message.text
    if await state.get_state() == 'promo_name_state':
        promos_dict[message.from_user.id]['promocode'] = var
        await bot.send_message(message.from_user.id, text= 'Введите цену')
        await state.set_state('promo_price_state')
    elif await state.get_state() == 'promo_price_state':
        promos_dict[message.from_user.id]['price'] = var
        await bot.send_message(message.from_user.id, text= 'Введите дату окончания в формате dd.mm.yyyy\n По умолчанию, промокод делается на год. Чтобы оставить значение по умолчанию, напишите 0')
        await state.set_state('promo_expire_date_state')
    elif await state.get_state() == 'promo_expire_date_state':
        promos_dict[message.from_user.id]['expire_date'] = var
        if datetime.strptime(var, '%d.%m.%Y').date() < datetime.now().date():
            await bot.send_message(message.from_user.id, text= 'Дата окончания не может быть меньше текущей даты')
            await state.set_state('promo_expire_date_state')
        else:
            await create_promo(message)
            
        await bot.send_message(message.from_user.id, text= 'Промокод создан')
        
        await marketer(message.from_user.id)
    else:
        await message.answer('Что-то пошло не так')
        
async def create_promo(message : types.Message):
    config = configparser.ConfigParser()
    config.read('config.ini') 
    bot_link = config.get('bot', 'link')
    promos_dict[message.from_user.id]['message.from_user.id'] = message.from_user.id  
    promos_dict[message.from_user.id]['referal'] = f'https://t.me/{bot_link}?start={message.from_user.id}_{promos_dict[message.from_user.id]["promocode"]}'
    await add_promocode(promos_dict[message.from_user.id])
    await message.answer(f'Промокод создан\nСсылка на промокод: `{promos_dict[message.from_user.id]["referal"]}`')
    await marketer(message.from_user.id)
    



dp.message.register(new_promo, StateFilter('promo_name_state', 'promo_price_state', 'promo_expire_date_state'))

dp.callback_query.register(callback_marketer, lambda c: c.data in ('my_promos', 'create_promo'))
