from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsAdmin
from keyboards.default import rmenu

from loader import dp


@dp.message_handler(IsAdmin(), text_contains="Отмена", state='*')
async def start_message_handler(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer("<b>🚀 Отменено</b>", reply_markup=rmenu.main_markup())








