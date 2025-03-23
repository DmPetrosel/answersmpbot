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
import logging, traceback
import asyncio
user_obj = {}
promos_dict = {}
promo_temp = {}
config = configparser.ConfigParser()
config.read('config.ini') 
bot_link = config.get('bot', 'link')
default_promo_name = "good_start"
DESCRIPTION = "🚀 Будьте эффективней. Отвечайте на отзывы быстрее и легче. \n\n💪 SSet АОтветы - бот для автоответов на ВБ"
async def marketer(message: types.Message, state: FSMContext, bot: MyBot):
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
    if not await get_promo_by_kwargs_last(chat_id=chat_id):
        await default_promo(message, state, bot)
    def_promo = await get_promo_by_kwargs_last(chat_id=chat_id)
    await bot.send_message(chat_id, f"{DESCRIPTION}\n\n<b>Ваш промокод:</b> <code>{def_promo.promocode}</code>\n💵 Сумма пополнения: <code>{def_promo.price} Р</code>\n📅 Дата окончания: <code>{(def_promo.expire_date).strftime('%d.%m.%Y')}</code>\n\n⚡️ Ссылка: <code>https://t.me/{bot_link}?start={def_promo.referal}</code>", parse_mode='html')
    msg = await bot.send_message(chat_id, f"ℹ️ Ваш промокод. Поделитесь им! 🗣 Вы получите 30% от первого пополнения реферала 💰, а реферал получит +20% к его сумме, если он оплатит сразу 💵.\n\nТакже вы можете создать промокоды на другую сумму.")
    await asyncio.sleep(20)
    await msg.delete()
async def default_promo(message : types.Message, state: FSMContext, bot):
    try:
        promos_dict[message.from_user.id] = {}
        promos_dict[message.from_user.id]['promocode'] = default_promo_name+"__"+str(message.chat.id)
        promos_dict[message.from_user.id]['price'] = int(("6 000").replace(' ','').replace('.','').replace(',',''))
        promos_dict[message.from_user.id]['expire_date'] = (datetime.now() + timedelta(days=14)).date()
        n_promo= await create_promo(message, state,  bot)
        p_name = (n_promo.promocode).split('__')[0] + str(n_promo.id)
        p_referal = (n_promo.referal).split('__')[0] + str(n_promo.id)
        result = await update_promo(id=n_promo.id, promocode=p_name, referal=p_referal)
    except Exception as e:
        logging.error(f"Error default_promo:59 {e} {traceback.print_exec}")
    return result
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
        if re.match('[a-z0-9_]', var.lower()):
            promos_dict[message.from_user.id]['promocode'] = var.lower()
            await bot.send_message(message.from_user.id, text= 'Введите сумму для пополнения.')
            await state.set_state('promo_price_state')
        else:
            await bot.send_message(message.from_user.id, text= 'Промокод должен состоять из латинских букв, цифр и символа подчеркивания')
            await state.set_state('promo_name_state')
    elif await state.get_state() == 'promo_price_state':
        promos_dict[message.from_user.id]['price'] = int(var.replace(' ','').replace('.','').replace(',','').strip())
        if promos_dict[message.from_user.id]['price'] < 0:
            await message.reply('Цена не может быть отрицательной. Введите сумму для пополнения ещё раз.')
            await state.set_state('promo_price_state')
            return
        await bot.send_message(message.from_user.id, text= 'Введите дату окончания в формате dd.mm.yyyy\n По умолчанию, промокод делается на год. Чтобы оставить значение по умолчанию, напишите 0')
        await state.set_state('promo_expire_date_state')
    elif await state.get_state() == 'promo_expire_date_state':
        promos_dict[message.from_user.id]['expire_date'] = var
        if var == '0':
            try:
                promos_dict[message.from_user.id]['expire_date'] = (datetime.now() + timedelta(days=365)).date()
            except Exception as e:
                logging.error(f"Error new_promo:105 {e} {traceback.print_exc()}")
        else:
            try: 
                date_var = datetime.strptime(var, '%d.%m.%Y')
                promos_dict[message.from_user.id]['expire_date'] = date_var.date()
            except Exception as e: 
                await bot.send_message(message.from_user.id, text= f'Дата должна быть в формате дд.мм.гггг.')
                state.set_state('expiering_date_state')
                return
            if datetime.strptime(var, '%d.%m.%Y').date() < datetime.now().date():
                await bot.send_message(message.from_user.id, text= 'Дата окончания не может быть меньше текущей даты')
                await state.set_state('promo_expire_date_state')
                return
            
        n_promo = await create_promo(message, state, bot)
        await bot.send_message(message.chat.id, f"{DESCRIPTION}\n\n<b>Ваш промокод:</b> <code>{n_promo.promocode}</code>\n💵 Пополнение на сумму: <code>{n_promo.price} Р</code>\n📅 Дата окончания: <code>{(n_promo.expire_date).strftime('%d.%m.%Y')}</code>\n\n⚡️ Ссылка: <code>https://t.me/{bot_link}?start={n_promo.referal}</code>", parse_mode='html')

    else:
        await message.answer('Что-то пошло не так')
        
async def edit_promo(message : types.Message, state: FSMContext, bot: MyBot):

    promocode_id = message.text.split('_')[-1]
    promocode_id = int(promocode_id)
    promos_dict[message.from_user.id] = {}
    prom = await get_promo_by_id(promocode_id)
    promos_dict[message.from_user.id]['promocode'] = prom.promocode
    promos_dict[message.from_user.id]['cdatetime.strptime(hat_id'] = prom.chat_id
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
async def create_promo(message : types.Message, state: FSMContext, bot :MyBot):
    promos_dict[message.from_user.id]['chat_id'] = message.from_user.id  
    promos_dict[message.from_user.id]['referal'] = f'{message.from_user.id}_{promos_dict[message.from_user.id]["promocode"]}'.replace(' ', '_')
    try:
        if promo_temp.get(message.chat.id) and promo_temp[message.from_user.id].get('is_updating'):
            promo_temp[message.from_user.id]['is_updating'] = False
            n_promo = await update_promo(promos_dict[message.from_user.id])
        else:
            n_promo = await add_promocode(promos_dict[message.from_user.id])
            return n_promo
    except SQLAlchemyError:
        await bot.send_message(message.chat.id, "Промокод не создан. Возможно, промокод с таким именем уже существует. Давайте попробуем ещё раз.\n\nВведите название промокода.")
        await state.set_state("promo_name_state")
        # await bot.send_message(message.chat.id, f"{DESCRIPTION}\n\n<b>Ваш промокод:</b> <code>{n_promo.promocode}</code>\n💵 Пополнение на сумму: <code>{n_promo.price} Р</code>\n📅 Дата окончания: <code>{(n_promo.expire_date).strftime('%d.%m.%Y')}</code>\n\n⚡️ Ссылка: <code>https://t.me/{bot_link}?start={n_promo.referal}</code>", parse_mode='html')
        return 
    await marketer(message,state, bot)
    

