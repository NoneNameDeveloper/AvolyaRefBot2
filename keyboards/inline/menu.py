from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from utils.db_api.models import Users, Buttons, Messages


def admin_main_markup():
    """
    основная панель админа
    """
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton("➕ Добавить админа", callback_data="add_admin"),
        InlineKeyboardButton("➖ Удалить админа", callback_data="del_admin")
    )
    markup.add(
        InlineKeyboardButton("👨‍💼 Изменить статус пользователя", callback_data="manipulateuser")
    )
    markup.add(
        InlineKeyboardButton("📨 Рассылка", callback_data="sending")
    )
    markup.add(
        InlineKeyboardButton("⏹ Изменить текст кнопок", callback_data="change_buttons")
    )
    markup.add(
        InlineKeyboardButton("⏹ Изменить текст сообщений", callback_data="change_messages")
    )
    markup.add(
        InlineKeyboardButton("⏹ Изменить условие 1 (кол-во)", callback_data="change|pdf_count_condition")
    )
    markup.add(
        InlineKeyboardButton("⏹ Изменить условие 2 (кол-во)", callback_data="change|video_count_condition")
    )
    markup.add(
        InlineKeyboardButton("⏹ Изменить условие 3 (кол-во)", callback_data="change|video_2_count_condition")
    )
    markup.add(
        InlineKeyboardButton("⏹ Изменить PDF", callback_data="change|pdf_content")
    )
    markup.add(
        InlineKeyboardButton("⏹ Изменить видео 1", callback_data="change|video_content")
    )
    markup.add(
        InlineKeyboardButton("⏹ Изменить видео 2", callback_data="change|video_2_content")
    )
    markup.add(
        InlineKeyboardButton("⏹ Изм. чат ID", callback_data="change|free_chat_id")
    )
    # markup.add(
    #     InlineKeyboardButton("⏹ Изм. Ссылку на чат", callback_data="change|free_chat_link")
    # )
    markup.add(
        InlineKeyboardButton("Таблица пользователей по реф. ссылке", callback_data="table_1")
    )
    markup.add(
        InlineKeyboardButton("Таблица пользователей обычных", callback_data="table_2")
    )
    markup.add(
        InlineKeyboardButton("Таблица админов", callback_data="table_4")
    )

    return markup


def user_status_markup(user_info):
    """
    блокировка/разблокировка/удаление пользователя
    """
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            text="🔒 Заблокировать" if not user_info.banned else "🔓 Разблокировать",
            callback_data=f"manipulate_{user_info.user_id}_block" if not user_info.banned else f"manipulate_{user_info.user_id}_unblock"
        ),
        InlineKeyboardButton(
            text="⚰️ Удалить",
            callback_data=f"manipulate_{user_info.user_id}_delete"
        ),
        InlineKeyboardButton(
            text="➕ Добавить реферала", callback_data=f"manipulate_{user_info.user_id}_add"
        )
    )

    return markup


def change_buttons_markup():
    """
    список кнопок для их изменений
    """
    markup = InlineKeyboardMarkup(row_width=2)

    btn_list = Buttons.get(Buttons.buttons_id == 1)

    for u in btn_list.__dict__['__data__'].keys():
        if '_id' not in u:
            markup.add(
                InlineKeyboardButton(
                    text=btn_list.__dict__['__data__'][u], callback_data=f"changebtn|{u}"
                )
            )

    return markup


def change_messages_markup():
    """
    список сообщений для их изменений
    """
    markup = InlineKeyboardMarkup(row_width=2)

    messages_list = Messages.get(Messages.messages_id == 1)

    for u in messages_list.__dict__['__data__'].keys():
        if '_id' not in u:
            markup.add(
                InlineKeyboardButton(
                    text=messages_list.__dict__['__data__'][u], callback_data=f"changemsg|{u}"
                )
            )

    return markup


def back_to_refs_markup():
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton("↩️ Назад", callback_data='back_to_refs')
    )

    return markup


def rate_markup():
    """
    вывод топ 10 рефоводов
    """
    markup = InlineKeyboardMarkup(row_width=2)

    buttons = Buttons.get(Buttons.buttons_id == 1)

    markup.add(
        InlineKeyboardButton(buttons.ref_list_button, callback_data="my_refs"),
        InlineKeyboardButton(buttons.rating_button, callback_data="rating")
    )

    return markup


def partner_markup(link):
    """
    поделиться партнерской ссылкой
    """
    markup = InlineKeyboardMarkup()

    buttons = Buttons.get(Buttons.buttons_id == 1)

    markup.add(
        InlineKeyboardButton(buttons.share_button, url=f"https://t.me/share/url?url={link}")
    )

    return markup


def paginate_top(data: list[Users], page: int = 0):
    """пагинация топа"""
    markup = InlineKeyboardMarkup()

    per_page = 10

    data = list(data)
    total_count = len(data)

    serv_btns = []

    # количество меньше или равно 10
    if len(data) <= per_page:
        print("None")
        return None

    if page > 0:
        serv_btns.append(
            InlineKeyboardButton(text="<<", callback_data=f"open_page|{page - 1}")
        )

    print(total_count)
    if total_count > (page+1) * per_page:
        serv_btns.append(
            InlineKeyboardButton(text=">>", callback_data=f"open_page|{page + 1}")
        )

    markup.add(*serv_btns)

    markup.add(
        InlineKeyboardButton("↩️ Назад", callback_data='back_to_refs')
    )

    return markup