import logging

from aiogram import Dispatcher, Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data.config import BOT_TOKEN
from middlewares.middleware import AuthenticationMiddleware

logging.basicConfig(level=logging.INFO)

bot = Bot(BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

# установка миддлвари для забаненных
auth = AuthenticationMiddleware()
dp.middleware.setup(auth)