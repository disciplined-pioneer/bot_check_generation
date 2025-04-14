from aiogram import Router, F
from aiogram.types import Message

from core.bot import bot
from settings import settings
from db.models.models import UserTopics


router = Router()


# Отправка сообщений в ЛС из топика
@router.message(F.chat.id == settings.bot.GROUP_ID)  # Используем фильтрацию по chat_id
async def handle_message_in_topic(message: Message):
    user = message.from_user
    if message.message_thread_id and not user.is_bot:  # Если сообщение из топика
        try:
            await bot.send_message(
                chat_id=user.id,
                text=message.text
            )
        except Exception as e:
            print(f"\nОшибка при отправке сообщения пользователю: {e}\n")


# Обработка сообщений от пользователя в ЛС
@router.message()
async def handle_message_from_user(message: Message):

    # Проверяем наличие топика
    user_topic = await UserTopics.get_by_tg_id(message.from_user.id)
    if not user_topic:
        await message.delete()  # Удаляем сообщение от пользователя
        return

    # Отправляем ответ обратно в нужный топик
    await bot.send_message(
        chat_id=settings.bot.GROUP_ID,
        message_thread_id=user_topic.topic_id,
        text=message.text
    )
