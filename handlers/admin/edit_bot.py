import os

from aiogram import types
from aiogram.dispatcher import FSMContext

from data import config
from keyboards.default import rmenu
from keyboards.inline import menu
from utils.db_api.models import Buttons, Messages, Users, Settings

from states.states import EditValue, EditBot, AddAdmin, DelAdmin

from loader import dp


@dp.callback_query_handler(text_contains="change_")
async def change_smth_handler(call: types.CallbackQuery):
    await call.answer()

    to_change = call.data.split('_')[1]

    if to_change == "buttons":
        await call.message.answer(
            text="Выберите кнопку для изменения из списка ниже.",
            reply_markup=menu.change_buttons_markup()
        )
    else:
        await call.message.answer(
            text="Выберите сообщение для изменения из списка ниже.",
            reply_markup=menu.change_messages_markup()
        )


@dp.callback_query_handler(text_contains="change|")
async def change_chat_1_handler(call: types.CallbackQuery, state: FSMContext):

    await call.answer()

    chat_value = call.data.split("|")[1]

    await state.finish()

    await EditValue.value_name.set()

    await state.update_data(value_name=chat_value)

    await EditValue.value_body.set()

    await call.message.answer("✍️ <b>Введите новое значение / отправьте файл или видео в бота.</b>", reply_markup=rmenu.cancel_admin_markup())


@dp.message_handler(state=EditValue.value_body, content_types=['animation', 'video', 'document', 'text'])
async def change_chat_2_handler(message: types.Message, state: FSMContext):

    data = await state.get_data()

    value = data['value_name']

    if value == 'pdf_content':
        if message.content_type == 'document':
            body = message.document.file_id
        else:
            return await message.answer("Неверный тип файла")

    elif value in ['video_content', 'video_2_content']:
        if message.content_type == 'video':
            body = message.video.file_id
        else:
            return await message.answer("Неверный тип файла")

    else:
        body = message.text

    stn = Settings.get(Settings.setting_id == 1)
    setattr(stn, value, body)
    stn.save()

    await state.finish()

    await message.answer("Успешно!", reply_markup=types.ReplyKeyboardRemove())


@dp.callback_query_handler(text_contains="changebtn|")
async def change_btn_1_handler(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    btn_name = call.data.split("|")[1]

    await state.finish()

    await EditBot.value_name.set()

    await state.update_data(value_name=btn_name)

    await EditBot.value_body.set()

    await call.message.answer("✍️ <b>Введите новый текст для кнопки.</b>", reply_markup=rmenu.cancel_admin_markup())


@dp.callback_query_handler(text_contains="changemsg|")
async def change_msg_1_handler(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    msg_name = call.data.split("|")[1]

    await state.finish()

    await EditBot.value_name.set()

    await state.update_data(value_name=msg_name)

    msg = Messages.get(Messages.messages_id == 1)
    text = getattr(msg, msg_name)

    await EditBot.value_body.set()

    await call.message.answer(f"✍️ Введите новый текст для сообщения.\n\n{text}", reply_markup=rmenu.cancel_admin_markup(), parse_mode=None)


@dp.message_handler(state=EditBot.value_body)
async def change_bot_handler(message: types.Message, state: FSMContext):

    data = await state.get_data()

    value = data['value_name']
    body = message.text

    # кнопка
    if "button" in value:
        btn = Buttons.get(Buttons.buttons_id == 1)
        setattr(btn, value, body)
        btn.save()

        await state.finish()

        await message.answer("Успешно!", reply_markup=types.ReplyKeyboardRemove())

    # сообщения
    else:
        msg = Messages.get(Messages.messages_id == 1)
        setattr(msg, value, body)
        msg.save()

        await state.finish()

        await message.answer("Успешно!", reply_markup=types.ReplyKeyboardRemove())


# Добавиление админа
@dp.callback_query_handler(chat_id=config.ADMINS, text="add_admin")
async def add_admin_init_handler(call: types.CallbackQuery, state: FSMContext):

    await call.answer()

    await AddAdmin.admin_id.set()

    await call.message.answer("🖊 Введите ID или @Username пользователя, которого вы хотите назначить админом.", reply_markup=rmenu.cancel_admin_markup())


@dp.message_handler(state=AddAdmin.admin_id)
async def add_admin_input(message: types.Message, state: FSMContext):

    # айди введен
    if message.text.isdigit():
        try:
            user = Users.get(Users.user_id == message.text)
        except:
            return await message.answer("Такого пользователя нет в базе!")

    # юзернейм введен
    else:
        try:
            user = Users.get(Users.username == message.text)
        except:
            return await message.answer("Такого пользователя нет в базе!")

    user.is_admin = True
    user.save()

    await state.finish()
    await message.answer("Админ добавлен!", reply_markup=types.ReplyKeyboardRemove())


# Удаление админа
@dp.callback_query_handler(chat_id=config.ADMINS, text="del_admin")
async def add_admin_init_handler(call: types.CallbackQuery):

    await call.answer()

    await DelAdmin.admin_id.set()

    await call.message.answer("🖊 Введите ID или @Username пользователя, которого вы хотите назначить админом.", reply_markup=rmenu.cancel_admin_markup())


@dp.message_handler(state=DelAdmin.admin_id)
async def add_admin_input(message: types.Message, state: FSMContext):

    # айди введен
    if message.text.isdigit():
        try:
            user = Users.get(Users.user_id == message.text)
        except:
            return await message.answer("Такого пользователя нет в базе!")

    # юзернейм введен
    else:
        try:
            user = Users.get(Users.username == message.text)
        except:
            return await message.answer("Такого пользователя нет в базе!")

    user.is_admin = False
    user.save()

    await state.finish()
    await message.answer("Админ удален!", reply_markup=types.ReplyKeyboardRemove())
#
#
# # Изменение таблицы Settings (сумма входа в чат, позиции реферальных бонусов)
# @dp.callback_query_handler(text="changeentrancesum")
# async def change_entrance_sum_1(call: types.CallbackQuery, state: FSMContext):
#
#     await call.answer()
#
#     await call.message.answer("✍️ Введиите новую сумму входа в приватный чат.", reply_markup=rmenu.cancel_admin_markup())
#
#     await EntranceSum.sum.set()
#
#
# @dp.message_handler(state=EntranceSum.sum)
# async def change_entrance_sum_2(message: types.Message, state: FSMContext):
#
#     if not message.text.isdigit():
#         return await message.answer("Введите целое число!")
#
#     settings = Settings.get(Settings.setting_id == 1)
#     settings.entrance_sum = message.text
#     settings.save()
#
#     await state.finish()
#     await message.answer("Сумма успешно установлена!", reply_markup=types.ReplyKeyboardRemove())
#
#
# @dp.callback_query_handler(text="changerefsum")
# async def change_entrance_sum_1(call: types.CallbackQuery, state: FSMContext):
#
#     await call.answer()
#
#     await call.message.answer("✍️ Введите номер позиции числом\n1 - 1-2\n2 - 3-9\n3 - 10+", reply_markup=rmenu.cancel_admin_markup())
#
#     await BonusSum.position.set()
#
#
# @dp.message_handler(state=BonusSum.position)
# async def change_entrance_sum_2(message: types.Message, state: FSMContext):
#
#     if not message.text.isdigit():
#         return await message.answer("Неверный ввод.")
#
#     if not int(message.text) in [1, 2, 3]:
#         return await message.answer("Неверный ввод.")
#
#     await state.update_data(position=int(message.text))  # целое число передается
#
#     await BonusSum.sum.set()
#
#     await message.answer("✍️ Введите сумму, на которую меняются начисляемый бонус (целое число, в рублях).")
#
#
# @dp.message_handler(state=BonusSum.sum)
# async def input_bons_sum_handler(message: types.Message, state: FSMContext):
#
#     if not message.text.isdigit():
#         return await message.answer("Введите целое число!")
#         # await state.finish()
#
#     data = await state.get_data()
#     data = data['position']
#     settings = Settings.get(Settings.setting_id == 1)
#
#     if data == 1:
#         settings.first_bonus = message.text
#     elif data == 2:
#         settings.second_bonus = message.text
#     else:
#         settings.third_bonus = message.text
#
#     settings.save()
#
#     await state.finish()
#     await message.answer("Данные успешно изменены!", reply_markup=types.ReplyKeyboardRemove())