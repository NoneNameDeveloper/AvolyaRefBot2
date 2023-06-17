from aiogram.types import ReplyKeyboardMarkup

from utils.db_api import Buttons


def main_markup():
    """
    основное реплай меню
    """
    buttons = Buttons.get(Buttons.buttons_id == 1)

    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(buttons.get_presents, buttons.chat_enter)
    markup.add(buttons.my_referrals, buttons.support)
    markup.add(buttons.telegram_game)

    return markup


def cancel_admin_markup():
    """
    отмена действий в админке
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row("❌ Отмена")

    return markup

