from create_bot import *
from db.get import *
from db.update import *
from aiogram import Dispatcher
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from keyboard.marketer_kb import *

async def callback_payout(call: types.CallbackQuery, state: FSMContext, bot: MyBot):
    if call.data.startswith("pout_confirm"):
        summa = call.data.split("_")[-1]
        call.message.edit_text("Введите реквизиты Российского банка:")
        await state.update_data(sum=summa)
        await state.set_state(P0ut.reqquisits)

async def payout_start(message: types.Message, state: FSMContext, bot: MyBot):
    user = await get_user(id=message.chat.id)
    bot.send_message(message.chat.id, f"Доступная сумма {user.payout} Р\n\nВведите сумму, которую хотите вывести или нажмите продолжить для вывода всей суммы.", reply_markup=await paysum_kb(user.payout))


def register_payout(dp: Dispatcher ):
    dp.callback_query.register(callback_payout, lambda c: c.data.startswith("pout_"))
    dp.message.register(payout_start, Command("payout"), StateFilter("*"))
    dp.message.register(payout_requisits)