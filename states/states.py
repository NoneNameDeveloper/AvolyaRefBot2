from aiogram.dispatcher.filters.state import StatesGroup, State


class EditBot(StatesGroup):
    value_name = State()
    value_body = State()


class EditValue(StatesGroup):
    value_name = State()
    value_body = State()


class SendingState(StatesGroup):
    text = State()


class ManipulateState(StatesGroup):
    user_id = State()


class AddAdmin(StatesGroup):
    admin_id = State()


class DelAdmin(StatesGroup):
    admin_id = State()


class EntranceSum(StatesGroup):
    sum = State()


class BonusSum(StatesGroup):
    position = State()
    sum = State()


class MoneyOut(StatesGroup):
    amount = State()
    data = State()


class DelBalance(StatesGroup):
    value = State()