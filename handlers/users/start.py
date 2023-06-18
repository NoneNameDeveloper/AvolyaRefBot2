from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from utils.misc import started_message

from loader import dp


@dp.message_handler(CommandStart(), chatstate='*', chat_type="private")
async def start_message_handler(message: types.Message, state: FSMContext):
    await state.finish()

    await started_message(message)
