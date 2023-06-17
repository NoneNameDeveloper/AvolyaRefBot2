from loader import dp
from data import config


async def create_link():
    return await dp.bot.create_chat_invite_link(chat_id=config.FREE_CHAT(), member_limit=100)