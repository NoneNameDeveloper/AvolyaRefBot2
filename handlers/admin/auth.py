from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsAdmin
from keyboards.inline import menu

from loader import dp


@dp.message_handler(IsAdmin(), text="/admin", state='*')
async def start_message_handler(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer(
        text="<b>👑 Добро пожаловать в панель админа.</b>",
        reply_markup=menu.admin_main_markup()
    )
