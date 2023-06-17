from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import menu
from utils.db_api.models import Buttons, Messages, Users, Moneyout

from states.states import SendingState

from loader import dp


@dp.callback_query_handler(text_contains="getout_")
async def money_out_admin_take_handler(call: types.CallbackQuery):

    await call.answer()

    data = call.data.split("_")

    out_id = data[1]

    moneyout = Moneyout.get(Moneyout.money_out_id == out_id)
    if not moneyout.admin_id:
        moneyout.admin_id = call.message.chat.id
        moneyout.admin_agree = True
        moneyout.admin_agree_date = datetime.now()
        moneyout.save()
        await call.message.answer("Нажмите кнопку ниже, когда осуществите вывод.", reply_markup=menu.admin_close_out_markup(out_id))
    else:
        await call.answer("Заявка уже в обработке.")


@dp.callback_query_handler(text_contains="closeout_")
async def money_out_close_handler(call: types.CallbackQuery):

    await call.answer()

    data = call.data.split("_")

    out_id = data[1]

    moneyout = Moneyout.get(Moneyout.money_out_id == out_id)

    moneyout.admin_payed = True
    moneyout.admin_payed_date = datetime.now()
    moneyout.save()
    await call.message.delete()
    await call.message.answer("Вывод закрыт с вашей стороны. Остается подтверждение пользователя.")

    await dp.bot.send_message(moneyout.user_id, "Админ подтвердил выполнение вывода. Проверьте поступление средств и нажмите кнопку ниже.", reply_markup=menu.user_agree_out(out_id))
