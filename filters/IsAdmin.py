from aiogram.dispatcher.filters import Filter
from aiogram import types

from data import config
from utils.db_api import Users


class IsAdmin(Filter):
    """
    кастомный фильтр

    проверка на то, что пользователь - админ
    """

    async def check(self, message: types.Message):
        user = Users.get(Users.user_id == message.chat.id)
        try:
            if user.is_admin or message.chat.id in config.ADMINS:
                return True
        except:
            return False
