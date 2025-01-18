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
from aiogram.filters.command import Command
import configparser
user_obj = {}
promos_dict = {}
promo_temp = {}
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
        dictionry = [f"Промокод: {i.promocode}\nЦена: {i.price}\nДата окончания: {i.expire_date}\nПереходы: {i.quantity}\nВаш ник: {i.user.username}\nИзменить промокод: /edit_promo_{i.id}\n\n" for i in promos_list]
        txt = ''.join(dictionry)
        await call.message.edit_text(f"Ваши промокоды: \n\n {txt}", parse_mode='html', reply_markup=marketer_menu_kb())
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
        promos_dict[message.from_user.id]['price'] = int(var.replace(' ','').replace('.','').replace(',',''))
        await bot.send_message(message.from_user.id, text= 'Введите дату окончания в формате dd.mm.yyyy\n По умолчанию, промокод делается на год. Чтобы оставить значение по умолчанию, напишите 0')
        await state.set_state('promo_expire_date_state')
    elif await state.get_state() == 'promo_expire_date_state':
        promos_dict[message.from_user.id]['expire_date'] = var
        if var == '0':
            promos_dict[message.from_user.id]['expire_date'] = (datetime.now() + timedelta(days=365)).strftime("%d.%m.%Y")
        else:
            try: 
                date_var = datetime.strptime(var, '%d.%m.%Y')
                promos_dict[message.from_user.id]['expire_date'] = date_var.strftime('%d.%m.%Y')
            except Exception as e: 
                await bot.send_message(message.from_user.id, text= f'Дата должна быть в формате дд.мм.гггг.')
                state.set_state('expiering_date_state')
            if datetime.strptime(var, '%d.%m.%Y').date() < datetime.now().date():
                await bot.send_message(message.from_user.id, text= 'А также дата окончания не может быть меньше текущей даты')
                await state.set_state('promo_expire_date_state')
            
        await create_promo(message)
            
    else:
        await message.answer('Что-то пошло не так')
        
async def create_promo(message : types.Message):
    config = configparser.ConfigParser()
    config.read('config.ini') 
    bot_link = config.get('bot', 'link')
    promos_dict[message.from_user.id]['chat_id'] = message.from_user.id  
    promos_dict[message.from_user.id]['referal'] = f'https://t.me/{bot_link}?start={message.from_user.id}_{promos_dict[message.from_user.id]["promocode"]}'
    if promo_temp[message.from_user.id]['is_updating']:
        promo_temp[message.from_user.id]['is_updating'] = False
        await update_promo(promos_dict[message.from_user.id])
    else:
        await add_promocode(promos_dict[message.from_user.id])
        await message.answer(f'Промокод создан\nСсылка на промокод: `{promos_dict[message.from_user.id]["referal"]}`')
    await marketer(message.from_user.id)
    
async def edit_promo(message : types.Message, state: FSMContext):

    promocode_id = message.text.split('_')[-1]
    promocode_id = int(promocode_id)
    promos_dict[message.from_user.id] = {}
    prom = await get_promo_by_id(promocode_id)
    promos_dict[message.from_user.id]['promocode'] = prom.promocode
    promos_dict[message.from_user.id]['chat_id'] = prom.chat_id
    promos_dict[message.from_user.id]['id'] = promocode_id
    promos_dict[message.from_user.id]['referal'] = prom.referal
    config = configparser.ConfigParser()
    config.read('config.ini') 
    support = config.get('support', 'support')
    promo_temp[message.from_user.id] = {}
    promo_temp[message.from_user.id]['obj'] = await get_promo_by_id(promocode_id)
    if promo_temp[message.from_user.id]['obj'].chat_id != message.from_user.id:
        message.edit_text(f"Вроде бы это не Ваш промокод. Если это ошибка, напишите: {support}")
    else:
        if promo_temp[message.from_user.id]:
            promos_dict[message.from_user.id]['promocode'] = promo_temp[message.from_user.id]['obj'].promocode
            promo_temp[message.from_user.id]['is_updating'] = True
            await bot.send_message(message.from_user.id, text= 'Введите новую цену')
            await state.set_state('promo_price_state')
        else:
            await message.answer('Промокод не найден')
            


dp.message.register(new_promo, StateFilter('promo_name_state', 'promo_price_state', 'promo_expire_date_state'))

dp.callback_query.register(callback_marketer, lambda c: c.data in ('my_promos', 'create_promo'))
dp.message.register(edit_promo, lambda c: c.text.startswith('/edit_promo'))