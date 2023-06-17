from aiogram import types

from keyboards.inline import menu
from utils.db_api import Users, Messages

from loader import dp


@dp.callback_query_handler(text="rating")
async def show_rate_handler(call: types.CallbackQuery):
    top_users: list[Users] = Users().get_top()

    text = "👑 Топ количества приглашённых\n\n"

    res = []

    for n, user in enumerate(top_users):

        count = Users.select().where(Users.active_referral_id == user.user_id).count()

        res.append([user.username, count])
        res.sort(key=lambda x: x[1], reverse=True)

    for n, data in enumerate(res):
        text += f'{n+1}) {data[0]} - {data[1]}\n'

    return await call.message.edit_text(
        text=text,
        reply_markup=menu.back_to_refs_markup()
    )


@dp.callback_query_handler(text="my_refs")
async def my_refs_list_handler(call: types.CallbackQuery):

    my_referrals: list[Users] = Users.select().where(Users.active_referral_id == call.message.chat.id)

    text = "Ваши приглашённые\n\n"

    for n, user in enumerate(my_referrals):
        text += f'{n+1}) {user.username}\n'

    return await call.message.edit_text(
        text=text,
        reply_markup=menu.back_to_refs_markup()
    )


@dp.callback_query_handler(text="back_to_refs")
async def back_to_main_refs(call: types.CallbackQuery):
    messages = Messages.get(Messages.messages_id == 1)

    await call.message.edit_text(
        text=messages.refs_list,
        reply_markup=menu.rate_markup()
    )
