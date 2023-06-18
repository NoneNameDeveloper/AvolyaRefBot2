from aiogram import types
from aiogram.types import InputFile
from openpyxl.workbook import Workbook

from utils.db_api.models import Users

from loader import dp


def users_dump(by_referal: bool = False, admin: bool = False, filename: str = "users.xlsx") -> str:
    """
    заполнение таблицы №1,2 - пользователи вошедшие по реф. ссылке и не по реф. ссылке
    """
    if admin:
        data = Users.select().where(Users.is_admin)
    elif by_referal:
        data = Users.select().where(Users.active_referral_id != 0).order_by(Users.date_time.desc())
    else:
        data = Users.select().where(Users.active_referral_id == 0).order_by(Users.date_time.desc())

    # Создание и заполнение файла Excel
    wb = Workbook()
    ws = wb.active

    # вошедшие по реф. ссылке
    if by_referal:
        ws.append(['User ID', 'ФИО', 'Username', 'Количество приглашенных', 'Дата входа в бота', 'реферер', 'Админ', 'ФИО Пригласившего', 'Username пригласившего'])

        for row in data:
            referal_data = Users.get(Users.user_id == row.active_referral_id)

            invited_count = Users.select().where(Users.active_referral_id == row.user_id).count()

            ws.append(
                [row.user_id, row.user_name, row.username, invited_count, row.date_time, row.active_referral_id,
                 row.is_admin, referal_data.user_name, referal_data.username])
    else:
        ws.append(['User ID', 'ФИО', 'Username', 'Количество приглашенных', 'Дата входа в бота', 'реферер', 'Админ'])

        for row in data:

            invited_count = Users.select().where(Users.active_referral_id == row.user_id).count()

            ws.append(
                [row.user_id, row.user_name, row.username, invited_count, row.date_time, row.active_referral_id, row.is_admin])

    # Сохранение файла
    wb.save(filename)

    return filename


@dp.callback_query_handler(text_contains="table_")
async def dump_tables_handler(call: types.CallbackQuery):

    await call.answer()
    table = int(call.data.split('_')[1])

    if table == 1:
        file = users_dump(by_referal=True, filename="ref_users.xlsx")
        return await call.message.answer_document(InputFile(file))
    elif table == 2:
        file = users_dump(by_referal=False, filename="default_users.xlsx")
        return await call.message.answer_document(InputFile(file))
    elif table == 4:
        file = users_dump(admin=True, filename="admins.xlsx")
        return await call.message.answer_document(InputFile(file))

    else:
        return
