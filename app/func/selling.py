from create_bot import *
from aiogram import types,  Dispatcher, handlers, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.filters.command import CommandObject
from db.set import *
from db.update import *
from db.get import *
import logging
from keyboard.basic_kb import *
from func.marketer_module import *
from func.states import *
from middleware import *
import traceback
from configparser import ConfigParser
import math
config = ConfigParser()

usr = {}
user_obj = {}
new_bot = {} # chat_id, token, bot_username, company_name, samples_ans, wb_token
cast_state = {}
config.read('config.ini')
user_cost = 176*2/10000*int(config.get('gigachat', 'ratio'))

async def start(message: types.Message, command: CommandObject, state: FSMContext):
    try:
        cast_state[message.chat.id] = {}
        await bot.send_message(message.from_user.id, "Привет, я бот для автоответов на ВБ\nПродолжая пользоваться ботом, вы соглашаетесь на обработку персональных данных.")
        if(await get_user(chat_id=message.from_user.id)):
            await bot.send_message(message.from_user.id, "Вы уже зарегистрированы! Здесь будут кнопки с меню. ")
            user_obj[message.from_user.id] = await get_user(message.from_user.id)
            if user_obj[message.from_user.id].marketer == True:
                print('Condition with is marketer passed ==============')
                await marketer(message, bot)
        else:

            usr[message.from_user.id] = {}
            print(f"=====\n\n{message.from_user.id} user id\n\n")
            usr[message.from_user.id]['promocode'] = None
            promo_obj = None
            try:
                arg = command.args
                print('=====', arg)
                if arg is not None:
                    promo_obj = await get_promo_by_kwargs(referal=arg)
            except Exception as e:
                print("Exception ", e)
            if promo_obj:
                usr[message.from_user.id]['referal'] = promo_obj.referal
                usr[message.from_user.id]['expire_date'] = promo_obj.expire_date
                usr[message.from_user.id]['promocode'] = promo_obj.promocode
                usr[message.from_user.id]['price'] = promo_obj.price
                print("Промокод найден")
            if promo_obj == None and arg is not None:
                await bot.send_message(message.from_user.id, "Промокод не найден! Вы сможете ввести его после имени.")
                usr[message.from_user.id]['referal'] = None
                usr[message.from_user.id]['expire_date'] = None
                usr[message.from_user.id]['promocode'] = None  
                usr[message.from_user.id]['price'] = None
            if promo_obj and promo_obj.expire_date != None and datetime.strptime(usr[message.from_user.id]['expire_date'], '%d.%m.%Y') < datetime.now():
                await bot.send_message(message.from_user.id, "Ваш промокод просрочен!")
                usr[message.from_user.id]['referal'] = None
                usr[message.from_user.id]['expire_date'] = None
                usr[message.from_user.id]['promocode'] = None
                usr[message.from_user.id]['price'] = None

            await registration(message, state)
    except Exception as e:
        logging.error(f"При запуске бота ошибка {e}")
async def registration(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Давайте зарегистрируемся!")
    usr[message.from_user.id]['marketer'] = False

    usr[message.from_user.id]['username'] = message.from_user.username
    if usr[message.from_user.id]['username'] == None: 
        await bot.send_message(message.from_user.id, "Введите никнейм")
        await state.set_state("username")
    else:
        await bot.send_message(message.from_user.id, "Введите имя")
        await state.set_state("first_name")
    

async def get_answer_reg(message : types.Message, state: FSMContext):
    var = message.text
    if await state.get_state() == 'username':
        usr[message.from_user.id]['username'] = var
        await bot.send_message(message.from_user.id, "Введите имя")
        await state.set_state("name")
    elif await state.get_state() == 'first_name':
        usr[message.from_user.id]['first_name'] = var
        if usr[message.from_user.id]['promocode'] == None:
            try:
                await bot.send_message(message.from_user.id, f"Введите промокод.", reply_markup=no_promo_kb())
                await state.set_state("promocode")
            except Exception as e:
                logging.error(f"{e}")
        else:
            await state.clear()
            await write_registration(message)

    elif await state.get_state() == 'promocode':   
        usr[message.from_user.id]['promocode'] = var.lower().strip()
        reg_success = False
        try:
            if var.lower().strip() == 'ямаркетолог' or var.lower().strip() == 'я маркетолог':
                usr[message.from_user.id]['marketer'] = True
                usr[message.from_user.id]['promocode'] = 'ямаркетолог'
                await state.clear()
            else:
                promo_obj = await get_promo_by_kwargs(promocode=usr[message.from_user.id]['promocode'])
                
                usr[message.from_user.id]['price'] = promo_obj.price

                if usr[message.from_user.id]['price'] == None:
                    await bot.send_message(message.from_user.id, 'Промокод не найден, попробуйте ещё раз: /start')
                    await state.set_state("promocode")
                else:
                    await state.clear()
            await write_registration(message)
            
        except Exception as e:
            logging.error(f"{e}")
    else:
        await bot.send_message(message.from_user.id, 'Что-то пошло не так, попробуйте ещё раз: /start')
    

async def write_registration(message :types.Message):
    chat_id = message.chat.id 
    logging.info(f"REGISTRATION DATA: {usr[chat_id]['username']}, {usr[chat_id]['first_name']}, {usr[chat_id]['promocode']}, {usr[chat_id]['marketer']}")
    if await add_user(chat_id=chat_id, username=usr[chat_id]['username'], first_name=usr[chat_id]['first_name'], promocode=usr[chat_id]['promocode'], marketer=usr[chat_id]['marketer']):
        await bot.send_message(chat_id, 'Регистрация прошла успешно')
    else:
        await bot.send_message(chat_id, str('Регистрация не удалась: \nВозможно, вы уже зарегистрированы'))
        return False
    user_obj[chat_id] = await get_user(chat_id)
    if user_obj[chat_id].marketer == True:
        await set_commands_marketer()
        await marketer(message, bot)
    else:
        await promo_continue(chat_id, usr[chat_id]['price'])
    return True
async def callback_selling(callback: types.CallbackQuery, state: FSMContext, bot: MyBot):
    config.read('config.ini')
    if callback.data == 'no_promo_call':
        price = config.get('price', 'default')
        usr[callback.from_user.id]['price'] = int(price)
        print("\n\n",callback.message.chat.id,"CB\n\n")
        await write_registration(callback.message)

    elif callback.data == 'pay_call':
        # await bot.send_message(callback.from_user.id, f"Оплата по ссылке {usr[callback.from_user.id]['price']}₽: <a href='yookassa.ru'>ЮКасса</a>", parse_mode='html')
        # await bot.send_message(callback.from_user.id, f"Продолжить без оплаты.", reply_markup=without_payment_kb())
        cast_state[callback.message.chat.id]['bonus'] = True
        await pay_start(callback=callback, state=state, amount=usr[callback.message.chat.id]['price'], bot=bot)
    elif callback.data == 'no_pay_call':
        cast_state[callback.message.chat.id]['bonus'] = False
        await bot.send_message(callback.from_user.id, f"Вы получили 300 бонусных рублей, для того, чтобы могли опробовать функции бота.")
        user = await get_user(callback.from_user.id)
        await update_user_by_id(id=user.id, balance=300)
        await bot.send_message(callback.from_user.id, 'Создайте бот в @botfather и вставьте сюда токен бота.', reply_markup=how_to_create_bot_kb())
        await state.set_state("get_bot_token")
    elif callback.data == 'how_to_create_bot_call':
        await callback.message.edit_text( '1. Переходим в @botfather.\n2. Вводим команду <code>/newbot</code>.\n3. Вводим имя бота и никнейм.\n4. Под этим текстом: "Use this token to access the HTTP API:" будет токен.\n5. Вставляем токен в бота АОтветы.\n\nОжидаю токен.',parse_mode='html')
        await state.set_state("get_bot_token")
    elif callback.data == 'mccancel_call':
        await state.clear()
        await callback.message.edit_text('Действие отменено.\n\nДля управления воспользуйтесь командами')
    elif callback.data.startswith('mcdel_bot_next_'):
        await callback.message.edit_text('Вы уверены, что хотите удалить бота?', reply_markup=del_bot_kb(int(callback.data.split('_')[-1])))
    elif callback.data.startswith('mcdel_bot_yes_'):
        await delete_bot(int(callback.data.split('_')[-1]))
        await callback.message.edit_text( 'Бот удалён. \n\nДля управления воспользуйтесь командами (меню)')
    elif callback.data.startswith('mcadd_manager_choose_them_'):
        tbot_data = await get_one_bot(id = int(callback.data.split('_')[-1]))
        await callback.message.edit_text(f'Выберете менеджера из списка. Если его в списке нет, вероятно, он не нажал кнопу старт в боте {tbot_data.bot_username}', reply_markup=await add_manager_list_kb(tbot_data.bot_username))    
    elif callback.data.startswith('mcadd_manager_next_'):
        bt = await get_one_bot(id=int(callback.data.split('_')[-2]))
        n = await get_bot_row(bot_username=bt.bot_username)
        success = await update_register(id=callback.data.split('_')[-1], approve = True, principal_chat_id=int(callback.message.chat.id))
        if success is not None:
            bot_list[n]['managers'].append(int(success.chat_id))
            await callback.message.edit_text( 'Менеджер добавлен.')
        else:
            await bot.send_message(callback.from_user.id, 'Что-то пошло не так, попробуйте ещё раз.')
    elif callback.data.startswith('mcdel_manager_choose_them_'):
        tbot = await get_one_bot(id=int(callback.data.split('_')[-1]))
        managers = await get_all_register(bot_username=tbot.bot_username)
        if managers:
            await callback.message.edit_text( 'Выберете менеджера для удаления', reply_markup=await del_manager_list_kb(tbot.bot_username))
        else:
            await callback.message.edit_text( 'Менеджеров нет.')
            
    elif callback.data.startswith('mcdel_manager_next_'):
        '''We get bot.id and then manager.id'''
        bt = await get_one_bot(id=int(callback.data.split('_')[-2]))
        n = await get_bot_row(bot_username=bt.bot_username)
        success = await update_register(id=callback.data.split('_')[-1], approve = False)
        if success is not None:
            logging.info(bot_list[n]['managers'])
            bot_list[n]['managers'].remove(success.chat_id)
            await callback.message.edit_text( 'Менеджер удалён.')
        else:
            await callback.message.edit_text( 'Что-то пошло не так, попробуйте ещё раз.')
            
            
    else:
        await bot.send_message(callback.from_user.id, 'Что-то пошло не так, попробуйте ещё раз: /start')
    
async def promo_continue(chat_id, price):
    await bot.send_message(chat_id, f'💵 Сумма пополнения: {price}\n'
                           f"Вы можете продолжить без оплаты. У вас будет 💵 300 бонусных рублей, чтобы попробовать функции. 😊\n\n"
                           f"✅ Но только при оплате сейчас вы получите в подарок 20% от оплаты.\n"
                           f"✅ Выгода +{float(price)*0.2}\n\n"
                           f"✅ Итого у вас будет: 💵 {float(price)*1.2} руб\n\n"
                           f"ℹ️ Оплата берётся за генерацию сообщения. Его стоимость зависит от длины сообщения.\n"
                           f"ℹ️ Средняя стоимость сообщения 2,5 Р\n"
                           f"ℹ️ 1 000 сообщений будут стоить около 2 500 рублей\n\n"
                           , reply_markup=promo_continue_kb())


async def get_bot_token(message: types.Message, state: FSMContext):
    result = await bot_init(token=message.text.strip(), chat_id=int(message.from_user.id), managers=[message.from_user.id])
    try:
        list_n, msgs = result
    except:
        list_n = result[0]
    new_bot[message.from_user.id] = {} # chat_id, token, bot_username, company_name, samples_ans, wb_token

    new_bot[message.from_user.id]['chat_id'] = int(message.from_user.id)
    new_bot[message.from_user.id]['token'] = message.text.strip()
    if list_n != None:
        try:
            new_bot[message.from_user.id]['bot_username'] = bot_list[list_n]['bot_username']
            if list_n is not None: await bot.send_message(message.from_user.id, f'Токен бота: {message.text.strip()}\n\n Теперь введите API-токен WB.\nОн должен быть сделан с возможностью записи чтобы можно было отвечать на WB отзывы. Должны быть подключены категории "Отзывы" и "Аналитика".')
            await bot_list[list_n]['bot'].send_message(message.from_user.id, f'Поздравляем, бот подключён!')
            await add_bot_info(new_bot[message.from_user.id])
            try:
                reg = await get_one_register(chat_id=int(message.from_user.id))
                if reg is not None:
                    await update_register(id=reg.id, chat_id=int(message.from_user.id), approve=True, principal_chat_id=int(message.chat.id))
                else: 
                    await add_register(chat_id=int(message.from_user.id), username= message.from_user.username, name = message.from_user.first_name, bot_username = bot_list[list_n]['bot_username'], approve=True)
                    bot_list[list_n]['managers'].append(message.from_user.id)                    
                await asyncio.sleep(10)
                if msgs is not None: 
                    for m in msgs: m.delete()
            except Exception as e:
                logging.error(f"{e}")
        except Exception as e:
            if list_n is None:
                await bot.send_message(message.from_user.id, f'Бот не подключён. \n\n{e}\n\n{traceback.print_exc()}\n\nПопробуйте ещё раз. \n\nВведите токен бота: ')
                await state.set_state("get_bot_token")    
        await state.set_state('get_wb_token')
    else:
        await bot.send_message(message.from_user.id, f'Бот не подключён. Попробуйте ещё раз. \n\nВведите токен бота: ')
        await state.set_state("get_bot_token")
async def get_wb_token(message: types.Message, state: FSMContext):
    list_n = await get_bot_row(chat_id=int(message.from_user.id))
    new_bot[message.from_user.id]['wb_token'] = message.text.strip()
    wb_token = message.text.strip()
    msg = await bot.send_message(message.chat.id, "Проверка токена, подождите.")
    ping = await get_ping(message.text.strip())
    if ping != 200:
        await bot.send_message(message.from_user.id, 'Токен ВБ не авторизован. Поменяйте токен или попробуйте ещё раз. Не забудьте дать разрешения на запись и категории: "Отзывы" и "Аналитика". Введите токен ещё раз.\n')       
        await state.set_state("get_wb_token")
        return
    if wb_token:
        await bot.send_message(message.from_user.id, f'API-токен WB: {message.text.strip()}')
        await bot.send_message(message.from_user.id, f'Поздравляем, бот подключён!')
        await bot.send_message(message.from_user.id, "Теперь введите название компании (магазина).")
        bot_list[list_n]['wb_token'] = wb_token
        await update_bot_info_dict_by_kw(new_bot[message.from_user.id], chat_id=int(message.from_user.id))
        await state.set_state(Form.company_name)
    else:
        await bot.send_message(message.from_user.id, f'Что-то пошло не так, возможно, проблема с токеном.')
    await msg.delete()
async def get_company_name(message: types.Message, state: FSMContext, bot: MyBot):
    new_bot[message.from_user.id]['company_name'] = message.text
    await update_bot_info_dict_by_kw(new_bot[message.from_user.id], bot_username=new_bot[message.from_user.id]['bot_username'])
    await bot.send_message(message.from_user.id, 'Введите описание и чем занимаетесь')
    await state.set_state(Form.description)

async def get_description(message: types.Message, state: FSMContext, bot: MyBot):
    new_bot[message.from_user.id]['company_description']= message.text
    await update_bot_info_dict_by_kw(new_bot[message.from_user.id], bot_username=new_bot[message.from_user.id]['bot_username'])
    await bot.send_message(message.from_user.id, "Описание и компания добавлены! Не забудьте добавить менеджеров в бота /addm . Менеждер, предварительно, должен нажать /start в Вашем боте.")
    await state.clear()

async def pay_command(message: types.Message, state: FSMContext, bot :MyBot):
    await state.clear()

    await bot.send_message(message.from_user.id, "💵 Введите суму в рублях, например: 3 000 или 2500")
    await state.set_state(PayState.enter_sum)

def payment(value:int,description:str):
    value = int(value)
    provider_data = {
          "receipt": {
            "items": [
              {
                "description": description,
                "quantity": "1.00",
                "amount": {
                  "value": f"{value:.2f}",
                  "currency": 'RUB'
                },
                "vat_code": 1

              }
            ]
          }
        }

    return json.dumps(provider_data)

async def pay_start(callback: types.Message, state: FSMContext, amount: int, bot: MyBot):
    await state.clear()
    amount_cop = int(amount * 100)
    config.read('config.ini')
    try:
            # Проверка состояния и его очистка
            current_state = await state.get_state()
            if current_state is not None:
                await state.clear()  # чтобы свободно перейти сюда из любого другого состояния

            if config.get('payment', 'yookassa').split(':')[1] == "TEST":
                await bot.send_message(callback.from_user.id, "Для оплаты используйте данные тестовой карты: 1111 1111 1111 1026, 12/22, CVC 000.")
            prices = [types.LabeledPrice(label='Оплата заказа', amount=amount_cop)]
            await state.set_state(PayState.buying)
            await bot.send_invoice(
                chat_id=callback.from_user.id,
                title='Пополнение баланса',
                description=f'Пополнение баланса.\n\n✅ Этой суммы примерно хватит для генерации {math.floor(amount/user_cost)} сообщений.\n🎁 Подарок: примерно {math.floor((amount*0.2)/user_cost)} сообщений.',
                payload='bot_paid',
                provider_token=config.get('payment', 'yookassa'),
                currency='RUB',
                prices=prices,
                need_phone_number=True,
                send_phone_number_to_provider=True,
                provider_data=payment(amount, f'Пополнение баланса на сумму {amount} Р.')
            )
    except Exception as e:
        logging.error(f"pay_start: Ошибка при выполнении команды /pay: {e}\n{traceback.print_exc()}")
        await bot.send_message(callback.from_user.id, "Произошла ошибка при обработке команды!")
        current_state = await state.get_state()
        if current_state is not None:
            await state.clear()



async def pay_sum(message: types.Message, state: FSMContext, bot: MyBot):
    await state.clear()
    if message.text is None:
        amount = int(usr[message.chat.id]['price'])
    else:
        amount = int(message.text.strip().replace(' ', '').replace('.', '').replace(',', ''))
    amount_cop = int(amount * 100)
    config.read('config.ini')
    try:
            if config.get('payment', 'yookassa').split(':')[1] == "TEST":
                await message.reply("Для оплаты используйте данные тестовой карты: 1111 1111 1111 1026, 12/22, CVC 000.")

            prices = [types.LabeledPrice(label='Оплата заказа', amount=amount_cop)]
            await state.set_state(PayState.buying)
            await bot.send_invoice(
                chat_id=message.chat.id,
                title='Пополнение баланса',
                description=f'Пополнение баланса.\n ✅ Этой суммы примерно хватит для генерации {math.floor(amount/user_cost)} сообщений.',
                payload='bot_paid',
                provider_token=config.get('payment', 'yookassa'),
                currency='RUB',
                prices=prices,
                need_phone_number=True,
                send_phone_number_to_provider=True,
                provider_data=payment(amount, f'Пополнение баланса на сумму {amount} Р.')
            )
    except Exception as e:
        logging.error(f"Ошибка при выполнении команды /pay: {e}")
        await message.answer("Произошла ошибка при обработке команды!")
        current_state = await state.get_state()
        if current_state is not None:
            await state.clear()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery, bot: MyBot):
    try:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)  # всегда отвечаем утвердительно
        logging.info('precheckout processing')
    except Exception as e:
        logging.error(f"Ошибка при обработке апдейта типа PreCheckoutQuery: {e}")

async def process_successful_payment(message: types.Message, state: FSMContext, bot :MyBot):
        await message.reply(f"Платеж на сумму {message.successful_payment.total_amount / 100} "
                            f"{message.successful_payment.currency} прошел успешно!")
        # await db.update_payment(message.from_user.id) TODO Сделать запись в БД
        logging.info(f"Получен платеж от {message.from_user.id}")
        await add_money_stat(chat_id = message.from_user.id, amount=(message.successful_payment.total_amount / 100), invoice_id=message.successful_payment.telegram_payment_charge_id, invoice_payload=message.successful_payment.invoice_payload)
        user = await get_user(message.from_user.id)
        data = cast_state.get(message.chat.id)
        ratio = 1
        if data.get("bonus") == True: ratio = 1.2
        await update_user_by_id(id=user.id, balance = user.balance + (message.successful_payment.total_amount / 100)*ratio)
        if user.is_payed_first_time == False:
            temp_promo = await get_promo_by_kwargs(promocode=user.promocode)
            await update_promo(id=temp_promo.id, quantity=temp_promo.quantity + 1)
            await update_user_by_id(id=temp_promo.user.id, balance = temp_promo.user.balance + ((message.successful_payment.total_amount / 100)*0.3), payout = temp_promo.user.payout + ((message.successful_payment.total_amount / 100)*0.3))
            await update_user_by_id(id=user.id, is_payed_first_time=True)
        current_state = await state.get_state()
        if current_state is not None:
            await state.clear()  # чтобы свободно перейти сюда из любого другого состояния
        if len(await get_all_bots(chat_id=message.chat.id)) == 0:
            await bot.send_message(message.chat.id, 'Создайте бот в @botfather и вставьте сюда токен бота.', reply_markup=how_to_create_bot_kb())
            await state.set_state("get_bot_token")
async def process_unsuccessful_payment(message: types.Message, state: FSMContext):
        await message.reply("Не удалось выполнить платеж!")
        current_state = await state.get_state()
        if current_state is not None:
            await state.clear()  # чтобы свободно перейти сюда из любого другого состояния
# async def check_payment(payment_id):
#      # Загружаем json текущим статусом
# 	payment = json.loads((Payment.find_one(payment_id)).json())
#     # Пингуем статус
# 	while payment['status'] == 'pending':
# 		payment = json.loads((Payment.find_one(payment_id)).json())
# 		await asyncio.sleep(3)
#         # Проверяем статус, если прошла то тру, иначе фолс
#         if payment['status']=='succeeded':
#             print("SUCCSESS RETURN")
#             print(payment)
            
#             return True
#         else:
#             print("BAD RETURN")
#             print(payment)
		
#             return False
# successful payment
# async def successful_payment(message: types.Message):
#     print("SUCCESSFUL PAYMENT:")
#     payment_info = message.successful_payment.to_python()
#     for k, v in payment_info.items():
#         print(f"{k} = {v}")

#     await bot.send_message(message.chat.id,
#                            f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")

def register_selling_handlers(dp: Dispatcher):
    dp.callback_query.register(callback_selling, lambda c: c.data in ('no_promo_call', 'pay_call', 'no_pay_call', 'how_to_create_bot_call', 'cancel_call') or c.data.startswith("mc"))
    dp.message.register(start, Command(commands=("start", "restart")), State(state="*"))
    dp.message.register(get_answer_reg, StateFilter('first_name', 'username', 'promocode'))
    dp.message.register(get_bot_token, StateFilter('get_bot_token'))
    dp.message.register(get_wb_token, StateFilter('get_wb_token'))
    # dp.callback_query.register(callback_selling, StateFilter('no_promo_call', 'pay_call' ))
    dp.message.register(pay_sum, StateFilter(PayState.enter_sum))
    dp.pre_checkout_query.register(process_pre_checkout_query)
    dp.message.register(process_successful_payment, F.successful_payment)
    dp.message.register(process_unsuccessful_payment, StateFilter(PayState.buying))
    dp.message.register(get_description, StateFilter(Form.description))
    dp.message.register(get_company_name, StateFilter(Form.company_name))
    # Marketer

    dp.message.register(new_promo, StateFilter('promo_name_state', 'promo_price_state', 'promo_expire_date_state'))

    dp.callback_query.register(callback_marketer, lambda c: c.data in ('my_promos', 'create_promo'))
    dp.message.register(edit_promo, lambda c: c.text.startswith('/edit_promo'))
async def main_bot():
    try:
        config.read('config.ini')
        await set_commands_main(bot)
        # dp.message.register(help, Command('help'), StateFilter('*'))
        dp.message.register(add_bot, Command('add'), StateFilter('*'))
        dp.message.register(delete_bot_ask, Command('delb'), StateFilter('*'))                    
        dp.message.register(add_manager, Command('addm'))                    
        dp.message.register(delete_manager, Command('delm'), StateFilter('*'))  
        dp.message.register(share_command, Command('balnshare'), StateFilter('*'))
        dp.message.register(pay_command, Command('pay'), StateFilter('*'))
        register_selling_handlers(dp)
        dp.message.outer_middleware(MyMiddleware(bot))
        await bot.send_message(chat_id=config['bot']['owner_id'],text='Bot started')
        await dp.start_polling(bot, skip_updates=False)
    except KeyboardInterrupt:
        logging.info('Bot stopped')
        print('SIGNAL Bot stopped. Goodbye!')
    finally:
        await bot.session.close()
        print("Main bot close")