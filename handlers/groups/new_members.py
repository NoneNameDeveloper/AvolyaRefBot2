from aiogram import types

from utils.db_api import Users, Settings

from loader import dp


@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def free_group_join_handler(message: types.Message):

	settings = Settings.get(Settings.setting_id == 1)

	if str(message.chat.id) == str(settings.free_chat_id):

		try:
			await message.delete()
		except:
			pass

		for member in message.new_chat_members:
			user_id = member.id

			user: Users = Users.get(Users.user_id == user_id)

			if user.referral_id:
				# активируем реферала
				Users.update({Users.active_referral_id: user.referral_id})\
					.where(Users.user_id == user_id)\
					.execute()

				settings = Settings.get(Settings.setting_id == 1)
				refed_count = Users.select().where(Users.active_referral_id == user.referral_id).count()

				if refed_count == settings.pdf_count_condition:
					await dp.bot.send_document(
						chat_id=user.referral_id,
						text=settings.pdf_content
					)
				elif refed_count == settings.video_count_condition:
					await dp.bot.video(
						chat_id=user.referral_id,
						text=settings.video_content
					)
				elif refed_count == settings.video_count_condition:
					await dp.bot.send_video(
						chat_id=user.referral_id,
						text=settings.video_2_content
					)