from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default import rmenu
from keyboards.inline import menu
from utils.db_api.models import Users

from states.states import ManipulateState, DelBalance

from loader import dp


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
            user = Users.get(Users.username == message.text)
        except:
            return await message.answer("Такого пользователя нет в базе!")

    await message.answer(f"""
🆔 Пользователь: {user.user_id}

👨‍🦰 Имя: {user.user_name}
🚪 Доступ: {user.entrance}
💰 Баланс: {user.balance}
""", reply_markup=menu.user_status_markup(user))

    await state.finish()


@dp.callback_query_handler(text_contains="manipulate_")
async def user_action_handler(call: types.CallbackQuery, state: FSMContext):

    await call.answer()

    action = call.data.split("_")[2]
    user_id = call.data.split("_")[1]

    user = Users.get(Users.user_id == user_id)
    if action == "block":
        user.banned = True
        user.save()

        await call.message.answer("Пользователь заблокирован!", reply_markup=types.ReplyKeyboardRemove())

    elif action == "unblock":
        user.banned = False
        user.save()
        await call.message.answer("Пользователь разблокирован!", reply_markup=types.ReplyKeyboardRemove())

    elif action == "delete":
        user.delete_instance()
        await call.message.answer("Пользователь удален из базы!", reply_markup=types.ReplyKeyboardRemove())

    elif action == "allow":
        user.entrance = True
        user.save()
        await call.message.answer("Пользователь получил доступ в чат!", reply_markup=types.ReplyKeyboardRemove())
    else:
        user.entrance = False
        user.save()
        await call.message.answer("Пользователь больше не имеет доступа в чат!", reply_markup=types.ReplyKeyboardRemove())

    await state.finish()


# вычитание баланса
@dp.callback_query_handler(text_contains="delbalance_")
async def minus_balance_from_user_1(call: types.CallbackQuery, state: FSMContext):

    await call.answer()

    user_id = call.data.split('_')[1]

    await call.message.answer("Введите сумму, на которую убавится баланс у пользователя.", reply_markup=rmenu.cancel_admin_markup())

    await DelBalance.value.set()
    await state.update_data(user_id=user_id)


@dp.message_handler(state=DelBalance.value)
async def del_balance_prod(message: types.Message, state: FSMContext):

    try:
        int(message.text)
    except:
        return await message.answer("Введите целое число!")

    data = await state.get_data()
    user_id = data['user_id']

    user_info = Users.get(Users.user_id == user_id)
    user_info.balance -= int(message.text)
    user_info.save()

    await message.answer("Успешно!", reply_markup=types.ReplyKeyboardRemove())
    return await state.finish()
