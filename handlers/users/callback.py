from aiogram import types

from keyboards.inline import menu
from utils.db_api import Users, Messages

from loader import dp


@dp.callback_query_handler(text="rating")
async def show_rate_handler(call: types.CallbackQuery):
    top_users: list[Users] = Users().get_top()

    page = 0

    top_users = list(top_users)
    top_users = top_users[page * 10:page * 10 + 10]

    text = "👑 Топ количества приглашённых\n\n"

    for n, user in enumerate(top_users):
        text += f'{n + 1}) {user[1]} - {user[-1]}\n'
        print(user)

    return await call.message.edit_text(
        text=text,
        reply_markup=menu.paginate_top(Users().get_top(), 0)
    )


@dp.callback_query_handler(text_contains="open_page|")
async def paginate_top_han(call: types.CallbackQuery):
    page = int(call.data.split("|")[1])

    top_users: list[Users] = list(Users().get_top())
    top_users = top_users[page * 10:page*10+10]

    text = "👑 Топ количества приглашённых\n\n"

    for n, user in enumerate(top_users):
        text += f'{n + 1 + page*10}) {user[1]} - {user[-1]}\n'

    return await call.message.edit_text(
        text=text,
        reply_markup=menu.paginate_top(Users().get_top(), page)
    )


@dp.callback_query_handler(text="my_refs")
async def my_refs_list_handler(call: types.CallbackQuery):

    my_referrals: list[Users] = Users.select().where(Users.active_referral_id == call.message.chat.id)

    text = "Ваши приглашённые\n\n" if len(my_referrals) > 0 else "У Вас пока 0 приглашённых."

    for n, user in enumerate(my_referrals):
        text += f'{n+1}) {user.user_name}\n'

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
