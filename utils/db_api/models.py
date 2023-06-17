import datetime

from peewee import *

from .connection import db


class Users(Model):
    user_id = BigIntegerField(null=False, primary_key=True)
    user_name = TextField()
    username = TextField()
    date_time = DateTimeField(null=False, constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')], default=datetime.datetime.now())
    referral_id = BigIntegerField(null=True)
    active_referral_id = BigIntegerField(null=False, default=0)
    is_admin = BooleanField(null=False, default=False)

    class Meta:
        database = db
        db_table = 'users'

    def get_top(self):
        """
        получить топ ппо количеству рфералов
        по заданному айди
        """
        users: list[Users] = Users.select(Users, fn.COUNT(Users.active_referral_id).alias('active_referral_id')) \
            .group_by(Users.user_id) \
            .order_by(fn.COUNT(Users.active_referral_id).desc()) \
            .limit(10)

        return users


class Settings(Model):
    setting_id = AutoField(primary_key=True, null=False)
    pdf_count_condition = IntegerField(null=False, default=1)
    video_count_condition = IntegerField(null=False, default=5)
    video_2_count_condition = IntegerField(null=False, default=20)
    pdf_content = TextField(null=False, default="https://google.com")
    video_content = TextField(null=False, default="https://google.com")
    video_2_content = TextField(null=False, default="https://google.com")
    free_chat_id = BigIntegerField(null=False, default=-100)
    free_chat_link = TextField(null=False, default="https://t.me/babodoy")

    class Meta:
        database = db
        db_table = 'settings'


class Buttons(Model):
    buttons_id = AutoField(primary_key=True, null=False)
    get_presents = TextField(default="получить подарки")
    chat_enter = TextField(default="вход в чат эфира")
    my_referrals = TextField(default="мои приглашенные")
    support = TextField(default="тех. поддержка")
    telegram_game = TextField(default="телеграм игра")
    rating = TextField(default="Топ")
    ref_list = TextField(default="Список приглашенных")
    share = TextField(default="Поделиться")

    class Meta:
        database = db
        db_table = 'buttons'


class Messages(Model):
    messages_id = AutoField(primary_key=True, null=False)
    start_message = TextField(default="""
Чтобы получить подарки воспользуйтесь кнопками из меню👇
""")
    get_presents = TextField(null=False, default="""
Получите подарки за приглашения❗️
1️⃣ Пригласив 2 друзей на эфир через этого бота вы получаете подарок - список из 30 полезных ботов в Телеграм❗️

2️⃣ Пригласив в 5 друзей, вы получаете видеозапись Станислава Санникова - “Эффектинвые методы работы в видеочате Телеграма”❗️

Ваша партнерская ссылка - <code>{ref_link}</code>

❗️Нажмите на ссылку 👆для копирования и приглашения своих друзей получайте подарки❗️
""")
    telegram_game = TextField(null=False, default="""Переходите в телеграм игру!""")
    enter_chat = TextField(null=False, default="""Добро пожаловать в чат""")
    support = TextField(null=False, default="""https://t.me/Teh_podderjhka""")
    refs_list = TextField(null=False, default="""Нажмите кнопки ниже для вывода информации..""")

    class Meta:
        database = db
        db_table = 'messages'

# db.drop_tables([Buttons])
# db.create_tables([Buttons])


# db.drop_tables([Users, Settings, Buttons, Messages])
# db.create_tables([Users, Settings, Buttons, Messages])
# #
# #
# Settings.create()
# Messages.create()
# Buttons.create()
