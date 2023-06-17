from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default import rmenu
from keyboards.inline import menu
from utils.db_api.models import Buttons, Messages, Users

from states.states import SendingState

from loader import dp


@dp.callback_query_handler(text_contains="sending")
async def sending_init_handler(call: types.CallbackQuery):

    await call.answer()
    await call.message.answer("Введите текст для рассылки.", reply_markup=rmenu.cancel_admin_markup())

    await SendingState.text.set()


@dp.message_handler(state=SendingState.text)
async def sending_input_handler(message: types.Message, state: FSMContext):

    users = Users.select()
    await message.answer("Рассылка началась.", reply_markup=types.ReplyKeyboardRemove())
    for u in users:
        good, bad = 0, 0
        try:
            await dp.bot.send_message(u.user_id, message.text)
            good += 1
        except:
            bad += 1

    await message.answer(f"Рассылка успешно завершилась!\nОтправлено: {good}\nНе отправлено: {bad}")

    await state.finish()
