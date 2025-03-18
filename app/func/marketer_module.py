from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.filters import StateFilter
from db.get import *
from keyboard.marketer_kb import *
from aiogram import types
from func.states import *
from datetime import datetime, timedelta
from db.set import *
import configparser
from aiogram.filters.command import Command
import configparser
import re
from aide import MyBot
import asyncio
user_obj = {}
promos_dict = {}
promo_temp = {}
config = configparser.ConfigParser()
config.read('config.ini') 
bot_link = config.get('bot', 'link')
default_promo_name = "good_start"
DESCRIPTION = "🚀 Будьте эффективней. Отвечайте на отзывы быстрее и легче. \n\n💪 SSet АОтветы - бот для автоответов на ВБ"
async def marketer(message: types.Message, bot: MyBot):
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
    chat_id = message.chat.id
    user_obj[chat_id] = await get_user(chat_id)
    balance = user_obj[chat_id].balance
    await bot.send_message(chat_id,  f"Ваш баланс: {balance}", reply_markup=marketer_menu_kb())
    msg = await bot.send_message(chat_id, f"Ваш промокод ниже. Также вы можете создать промокоды на другую сумму.")
    if not await get_promo_by_kwargs(chat_id=chat_id):
        await default_promo(message, bot)
    def_promo = await get_promo_by_kwargs(chat_id=chat_id, promocode=default_promo_name)
    await bot.send_message(chat_id, f"{DESCRIPTION}\n\n<b>Ваш промокод:</b> <code>{def_promo.promocode}</code>\n💵 Цена: <code>6 000 к</code>\n📅 Дата окончания: <code>{(def_promo.expire_date).strftime('%d.%m.%Y')}</code>\n\n⚡️ Ссылка: <code>https://t.me/{bot_link}?start={def_promo.referal}</code>", parse_mode='html')
    await asyncio.sleep(12)
    await msg.delete()
async def default_promo(message : types.Message, bot):
    promos_dict[message.from_user.id] = {}
    promos_dict[message.from_user.id]['promocode'] = default_promo_name
    promos_dict[message.from_user.id]['price'] = int(("6 000").replace(' ','').replace('.','').replace(',',''))
    promos_dict[message.from_user.id]['expire_date'] = (datetime.now() + timedelta(days=14)).date()
    await create_promo(message, bot)
    return
async def callback_marketer(call: types.CallbackQuery, state: FSMContext, bot: MyBot):
    # await call.answer(cache_time=60)
    print('callback marketer')
    if call.data == 'my_promos':
        promos_list = await get_all_promos(call.from_user.id)
        dictionry = [f"Промокод: {i.promocode}\nЦена: {i.price}\nДата окончания: {i.expire_date}\nПереходы: {i.quantity}\nВаш ник: {i.user.username}\nCсылка: <code>https://t.me/{bot_link}?start={i.referal}</code>\n[Изменить промокод /edit_promo_{i.id}]\n\n" for i in promos_list]

        txt = ''.join(dictionry)
        await call.message.edit_text(f"Ваши промокоды: \n\n {txt}", reply_markup=marketer_menu_kb(), parse_mode='html')
    elif call.data == 'create_promo':
        promos_dict[call.from_user.id] = {}
        await call.message.edit_text('Введите промокод')
        await state.set_state('promo_name_state')
    #     promocodes = await get_promocodes(call.from_user.id)
    #     if promocodes:
    #         await call.message.edit_text(f"Ваши промокоды: \n{promocodes}", reply_markup=marketer_menu_kb)

async def new_promo(message:types.Message, state: FSMContext, bot: MyBot):
    var = message.text
    if await state.get_state() == 'promo_name_state':
        if re.match('[a-z0-9_ ]', var.lower()):
            promos_dict[message.from_user.id]['promocode'] = var.lower()
            await bot.send_message(message.from_user.id, text= 'Введите цену')
            await state.set_state('promo_price_state')
        else:
            await bot.send_message(message.from_user.id, text= 'Промокод должен состоять из латинских букв, цифр и символа подчеркивания')
            await state.set_state('promo_name_state')
    elif await state.get_state() == 'promo_price_state':
        promos_dict[message.from_user.id]['price'] = int(var.replace(' ','').replace('.','').replace(',',''))
        await bot.send_message(message.from_user.id, text= 'Введите дату окончания в формате dd.mm.yyyy\n По умолчанию, промокод делается на год. Чтобы оставить значение по умолчанию, напишите 0')
        await state.set_state('promo_expire_date_state')
    elif await state.get_state() == 'promo_expire_date_state':
        promos_dict[message.from_user.id]['expire_date'] = var
        if var == '0':
            promos_dict[message.from_user.id]['expire_date'] = (datetime.now() + timedelta(days=365)).date()
            await create_promo(message, bot)
        else:
            try: 
                date_var = datetime.strptime(var, '%d.%m.%Y')
                promos_dict[message.from_user.id]['expire_date'] = date_var.date()
            except Exception as e: 
                await bot.send_message(message.from_user.id, text= f'Дата должна быть в формате дд.мм.гггг.')
                state.set_state('expiering_date_state')
            if datetime.strptime(var, '%d.%m.%Y').date() < datetime.now().date():
                await bot.send_message(message.from_user.id, text= 'Дата окончания не может быть меньше текущей даты')
                await state.set_state('promo_expire_date_state')
            else:
                await create_promo(message, bot)
            
    else:
        await message.answer('Что-то пошло не так')
        
async def create_promo(message : types.Message, bot :MyBot):
    promos_dict[message.from_user.id]['chat_id'] = message.from_user.id  
    promos_dict[message.from_user.id]['referal'] = f'{message.from_user.id}_{promos_dict[message.from_user.id]["promocode"]}'.replace(' ', '_')
    try:
       promo_temp[message.from_user.id]['is_updating']
    except:
        promo_temp = {}
        promo_temp[message.from_user.id] = {}
        promo_temp[message.from_user.id]['is_updating'] = False 
    if promo_temp[message.from_user.id]['is_updating']:
        promo_temp[message.from_user.id]['is_updating'] = False
        await update_promo(promos_dict[message.from_user.id])
    else:
        await add_promocode(promos_dict[message.from_user.id])
        await message.answer(f'Промокод создан\nСсылка на промокод: <code>https://t.me/{bot_link}?start={promos_dict[message.from_user.id]["referal"]}</code>', parse_mode='html')
        return
    await marketer(message.from_user.id, bot)
    
async def edit_promo(message : types.Message, state: FSMContext, bot: MyBot):

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
            

