from loguru import logger

from aiogram import executor
from aiogram.types import BotCommand

import handlers

from loader import dp


async def on_startup(_):
    try:
        await dp.bot.send_message(1888872438, "Started!")
    except:
        logger.error("Started message failed")

    bot_commands = [
        BotCommand(command="/start", description="перезапуск")
    ]
    await dp.bot.set_my_commands(bot_commands)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)