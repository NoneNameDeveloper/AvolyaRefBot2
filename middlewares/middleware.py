from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import Message
from loguru import logger

from utils.db_api import Users


class AuthenticationMiddleware(BaseMiddleware):
    async def on_process_message(self, message: Message, data: dict):

        if message.chat.type != "private":
            raise CancelHandler()

        user_id = message.chat.id
        logger.debug(f'New message from @{message.from_user.username}:{user_id}')

        user_info = Users.get_or_none(Users.user_id == user_id)

        if not user_info:
            if not message.text == "/start":
                return await message.answer("Введите /start")
            else:
                return logger.error(f"user @{message.from_user.username} is not authorized..")

        if user_info.banned:
            raise CancelHandler()



