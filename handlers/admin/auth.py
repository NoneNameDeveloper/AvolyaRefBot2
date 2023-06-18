from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsAdmin
from keyboards.inline import menu

from loader import dp
from utils.db_api import Settings


@dp.message_handler(IsAdmin(), text="/admin", state='*')
async def start_message_handler(message: types.Message, state: FSMContext):
    await state.finish()

    settings = Settings.get(Settings.setting_id == 1)

    await message.answer(
        text=f"""
<b>👑 Добро пожаловать в панель админа.</b>

Пороги призов: {settings.pdf_count_condition}/{settings.video_count_condition}/{settings.video_2_count_condition}
""",
        reply_markup=menu.admin_main_markup()
    )
