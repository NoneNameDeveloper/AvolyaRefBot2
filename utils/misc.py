from aiogram import types
from loguru import logger

from keyboards.default import rmenu
from loader import dp

from utils.db_api import Messages, Users, Settings


async def started_message(message: types.Message):
    """
    стартовое сообщение (/start)
    """
    # регистрация пользователя
    await register_user(message)

    messages = Messages.get(Messages.messages_id == 1)

    await message.answer(
        text=messages.start_message,
        reply_markup=rmenu.main_markup()
    )


async def register_user(message: types.Message):
    """
    регистрация пользователя
    """
    check_user = Users.get_or_none(Users.user_id == message.chat.id)

    # если пользователя нет в базе
    if not check_user:
        args = message.get_args().split()

        # от реферала
        if args and args[0] != message.chat.id and args[0].isdigit():
            Users.create(
                user_id=message.chat.id,
                user_name=message.from_user.full_name,
                username="@" + str(message.from_user.username),
                referral_id=int(args[0])
            )

            logger.debug(f'user registered: @{message.from_user.username}:{message.from_user.id}. Refed from: {args[0]}')

        else:
            Users.create(
                user_id=message.chat.id,
                user_name=message.from_user.full_name,
                username="@" + str(message.from_user.username)
            )

            logger.debug(f'user registered: @{message.from_user.username}:{message.from_user.id}')

    return
