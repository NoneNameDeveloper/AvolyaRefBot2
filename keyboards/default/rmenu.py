from aiogram.types import ReplyKeyboardMarkup

from utils.db_api import Buttons


def main_markup():
    """
    основное реплай меню
    """
    buttons = Buttons.get(Buttons.buttons_id == 1)

    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(buttons.get_presents_button, buttons.chat_enter_button)
    markup.add(buttons.my_referrals_button, buttons.support_button)
    markup.add(buttons.telegram_game_button)

    return markup


def cancel_admin_markup():
    """
    отмена действий в админке
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row("❌ Отмена")

    return markup

