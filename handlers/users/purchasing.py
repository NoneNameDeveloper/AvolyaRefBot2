from datetime import datetime


from aiogram import types
from aiogram.dispatcher import FSMContext
from yookassa import Configuration, Payment

from data import config
from data.config import MessagesList
from keyboards.default import rmenu
from keyboards.inline import menu
from utils.db_api.models import Settings, Users

from loader import dp


@dp.callback_query_handler(text="buy_entrance")
async def buy_entrance_handler(call: types.CallbackQuery):

    settings = Settings.get(Settings.setting_id == 1)
    # сумма входа в чат
    entrance_sum = str(round(settings.entrance_sum))

    await call.message.answer(f"""
📋 <b>Выберите удобный Вам метод оплаты из предложенных ниже</b>

💸 <i>Сумма к оплате: {entrance_sum} ₽</i>
""", reply_markup=menu.choose_payment_method())


@dp.callback_query_handler(text_contains="buy_")
async def choose_country_buy_method(call: types.CallbackQuery):
    data = call.data.split("_")[1]

    settings = Settings.get(Settings.setting_id == 1)
    # сумма входа в чат
    entrance_sum = (round(settings.entrance_sum))

    if data == "rf":
        await call.message.answer(f"""
📋 <b>Выберите удобный Вам метод оплаты из предложенных ниже</b>

💸 <i>Сумма к оплате: {entrance_sum} ₽</i>
""", reply_markup=menu.choose_payment_method_rf())

    # stripe
    if data == "norf":
        NOMENKLATURE_TEXT = "Покупка доступа в чат"
        prices = [types.LabeledPrice(NOMENKLATURE_TEXT, entrance_sum * 100)]

        payload = f"{call.message.chat.id}_{entrance_sum}"

        try:
            # отправляем счет на оплату
            await dp.bot.send_invoice(
                chat_id=call.message.chat.id,
                title=NOMENKLATURE_TEXT,
                description="\n\n",
                payload=payload,
                provider_token=config.STRIPE_API,
                currency="rub",
                prices=prices,
            )
        except Exception as e:
            print(e)
            await call.message.answer('Введите корректную сумму.')


@dp.pre_checkout_query_handler(state='*')
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):

    await dp.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(state='*', content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message, state: FSMContext):

    await state.finish()

    payment = message.successful_payment.to_python()
    payload = payment['invoice_payload']

    chat_id = message.chat.id

    paymet_sum = payment['total_amount'] / 100

    user = Users.get(Users.user_id == chat_id)
    ref_id = user.referral_id
    user.payment_sum = paymet_sum
    user.payment_date = datetime.now()
    user.payment_type = "STRIPE"
    user.entrance = True
    user.save()

    if ref_id:
        settings = Settings.get(Settings.setting_id == 1)
        refs_count = Users.select().where((Users.referral_id == ref_id) & (Users.entrance == True)).count()

        if 1 <= refs_count <= 2:
            bonus = settings.first_bonus
        elif 3 <= refs_count <= 9:
            bonus = settings.second_bonus
        elif refs_count >= 10:
            bonus = settings.third_bonus
        else:
            bonus = 0

        ref_sum = bonus  # пополнение баланса тому, кто пригласил купишего пользователя

        refman = Users.get(Users.user_id == ref_id)
        refman.balance += ref_sum
        refman.save()

        await dp.bot.send_message(ref_id, MessagesList.main_menu_messages()[8].replace("{sum}", str(ref_sum)))

    link_to_chat = await dp.bot.create_chat_invite_link(config.PAY_CHAT(), member_limit=1)

    await message.answer(MessagesList.main_menu_messages()[10], reply_markup=rmenu.main_markup())
    await message.answer_photo(photo=MessagesList.main_menu_messages()[11],
                                    caption=MessagesList.main_menu_messages()[9],
                                    reply_markup=menu.private_entrance_markup(link_to_chat.invite_link))


@dp.callback_query_handler(text_contains="method|")
async def choose_pay_method_handler(call: types.CallbackQuery):
    # await call.answer()

    method = call.data.split("|")[1]

    chat_id = call.message.chat.id

    settings = Settings.get(Settings.setting_id == 1)
    # сумма входа в чат
    entrance_sum = str(round(settings.entrance_sum))

    bot_data = await dp.bot.get_me()
    bot_username = bot_data.username

    success_url = 'https://t.me/%s?start=%s' % (bot_username, str(chat_id))

    Configuration.configure("315589", "live_D9-KYv8I76lGaHll0ZNrEkMMKUu-sE2wF8UShxrUhWE")

    try:
        if method != "sbp":
            payment = Payment.create({
                "amount": {
                    "value": entrance_sum,
                    "currency": "RUB"
                },
                "payment_method_data": {
                    "type": method,

                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": success_url
                },
                "description": "Покупка доступа в чат"
            })
        else:
            payment = Payment.create({
                "amount": {
                    "value": entrance_sum,
                    "currency": "RUB"
                },
                "payment_method_data": {
                    "type": method,

                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": success_url
                },
                "capture": True,
                "description": "Покупка доступа в чат"
            })
    except Exception as e:
        return await call.answer("Данный метод сейчас не доступен, выберите, пожалуйста, другой.")

    await call.message.delete()

    await call.message.answer("""
1. Перейдите по ссылке на оплату.
2. Проведите оплату.
3. Дождитесь положительного ответа от платежной системы.
4. Вернитесь в бота и нажмите кнопку "🔒 Проверить оплату".
""", reply_markup=menu.pay_markup(payment.confirmation.confirmation_url, payment.id))


@dp.callback_query_handler(state='*', text_contains="check_payment_")
async def process_successful_payment(call: types.CallbackQuery):

    payment_id = call.data.split("_")[2]
    Configuration.configure(config.WALLET, config.UKASSA_API)
    payment = Payment.find_one(payment_id)
    payment_method = payment.payment_method.type
    if payment.status == "pending":
        return await call.answer("Средства еще не поступили!")

    await call.answer()

    if payment.status == "waiting_for_capture" or payment_method == "sbp":
        if payment_method != "sbp":
            response = Payment.capture(
                payment_id,
                {
                    "amount": {
                        "value": payment.amount.value,
                        "currency": "RUB"
                    }
                }
            )
            paid = response.paid
        else:
            paid = True

        if paid or payment_method == "sbp":

            chat_id = call.message.chat.id

            paymet_sum = payment.amount.value

            user = Users.get(Users.user_id == chat_id)
            ref_id = user.referral_id
            user.payment_sum = paymet_sum
            user.payment_date = datetime.now()
            user.payment_type = "ЮКАССА"
            user.entrance = True
            user.save()

            await call.message.delete()

            if ref_id:
                settings = Settings.get(Settings.setting_id == 1)
                refs_count = Users.select().where(Users.referral_id == ref_id).count()

                if 1 <= refs_count <= 2:
                    bonus = settings.first_bonus
                elif 3 <= refs_count <= 9:
                    bonus = settings.second_bonus
                elif refs_count >= 10:
                    bonus = settings.third_bonus
                else:
                    bonus = 0

                ref_sum = bonus  # пополнение баланса тому, кто пригласил купишего пользователя

                refman = Users.get(Users.user_id == ref_id)
                refman.balance += ref_sum
                refman.save()

                await dp.bot.send_message(ref_id, MessagesList.main_menu_messages()[8].replace("{sum}", str(ref_sum)))

            link_to_chat = await dp.bot.create_chat_invite_link(config.PAY_CHAT(), member_limit=1)

            await call.message.answer(MessagesList.main_menu_messages()[10], reply_markup=rmenu.main_markup())
            await call.message.answer_photo(photo=MessagesList.main_menu_messages()[11], caption=MessagesList.main_menu_messages()[9], reply_markup=menu.private_entrance_markup(link_to_chat.invite_link))

