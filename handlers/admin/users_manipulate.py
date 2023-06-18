import random

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default import rmenu
from keyboards.inline import menu
from utils.db_api.models import Users

from states.states import ManipulateState, DelBalance

from loader import dp
from utils.misc import give_prize


@dp.callback_query_handler(text_contains="manipulateuser")
async def sending_init_handler(call: types.CallbackQuery):

    await call.answer()
    await call.message.answer("✍️ Введите ID или @Username пользователя, для изменения его статуса в боте.", reply_markup=rmenu.cancel_admin_markup())

    await ManipulateState.user_id.set()


@dp.message_handler(state=ManipulateState.user_id)
async def manipulate_main_handler(message: types.Message, state: FSMContext):

    # айди введен
    if message.text.isdigit():
        try:
            user = Users.get(Users.user_id == message.text)
        except:
            return await message.answer("Такого пользователя нет в базе!")

    # юзернейм введен
    else:
        try:
            user: Users = Users.get(Users.username == message.text)
        except:
            return await message.answer("Такого пользователя нет в базе!")

    await message.answer(f"""
🆔 Пользователь: {user.user_id}

👨‍🦰 Имя: {user.user_name}
🔐 Забанен: {user.banned}
""", reply_markup=menu.user_status_markup(user))

    await state.finish()


@dp.callback_query_handler(text_contains="manipulate_")
async def user_action_handler(call: types.CallbackQuery, state: FSMContext):

    action = call.data.split("_")[2]
    user_id = call.data.split("_")[1]

    user: Users = Users.get(Users.user_id == user_id)
    if action == "block":
        user.banned = True
        user.save()

        await call.message.answer("Пользователь заблокирован!", reply_markup=types.ReplyKeyboardRemove())

    elif action == "unblock":
        user.banned = False
        user.save()
        await call.message.answer("Пользователь разблокирован!", reply_markup=types.ReplyKeyboardRemove())

    elif action == "delete":
        print(user_id)
        row_count_mod = Users.update({Users.active_referral_id: 0}).where(Users.active_referral_id == user_id).execute()
        print(row_count_mod)
        user.delete_instance()
        await call.message.answer("Пользователь удален из базы!", reply_markup=types.ReplyKeyboardRemove())

    # добавление реферала пользователю
    elif action == "add":
        Users.create(
            user_id="000" + str(random.randint(99999, 99999999999999)),
            user_name="None",
            username="None",
            referral_id=None,
            active_referral_id=user_id,
            is_admin=False,
            banned=False
        )

        refs_count = Users.select().where(Users.active_referral_id == user_id).count()

        await call.message.answer(f"Реферал добавлен! Количество рефералов у пользователя - {refs_count}")

        await give_prize(user_id)

    await call.answer()
    await state.finish()
