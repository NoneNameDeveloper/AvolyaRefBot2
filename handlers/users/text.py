from aiogram import types

from keyboards.inline import menu
from loader import dp
from utils.db_api import Users, Buttons, Messages


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def text_handler(message: types.Message):
    chat_id = message.chat.id

    buttons = Buttons.get(Buttons.buttons_id == 1)
    messages = Messages.get(Messages.messages_id == 1)

    # получить подарки
    if message.text == buttons.get_presents:
        bot_ = await dp.bot.get_me()
        bot_username = bot_.username
        link = f"https://t.me/{bot_username}?start={chat_id}"

        await message.answer(messages.get_presents.replace(
                "{ref_link}", link
            ),
            reply_markup=menu.partner_markup(link)
        )

    # вход в чат эфира
    elif message.text == buttons.chat_enter:
        await message.answer(text=messages.enter_chat)

    # мои приглашенные
    elif message.text == buttons.my_referrals:
        await message.answer(
            text=messages.refs_list,
            reply_markup=menu.rate_markup()
        )

    # тех.подержка
    elif message.text == buttons.support:
        await message.answer(messages.support)

    # телеграм игра
    elif message.text == buttons.telegram_game:
        await message.answer(messages.telegram_game)



