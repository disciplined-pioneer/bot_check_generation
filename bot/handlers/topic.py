from aiogram import Router, F
from aiogram.types import Message, InputFile
from core.bot import bot
from settings import settings
from db.models.models import UserTopics

router = Router()


# Отправка сообщений в ЛС из топика
@router.message(F.chat.id == settings.bot.GROUP_ID)
async def handle_message_in_topic(message: Message):
    user = message.from_user
    topic_id = message.message_thread_id
    tg_id = await UserTopics.get_topic_id_by_tg_id(topic_id)
    if topic_id and not user.is_bot:
        try:
            # Текст
            if message.text:
                await bot.send_message(chat_id=tg_id, text=message.text)

            # Фото
            elif message.photo:
                await bot.send_photo(
                    chat_id=tg_id,
                    photo=message.photo[-1].file_id,  # Самое большое по размеру
                    caption=message.caption or ""
                )

            # Документ
            elif message.document:
                await bot.send_document(
                    chat_id=tg_id,
                    document=message.document.file_id,
                    caption=message.caption or ""
                )

            # Видео
            elif message.video:
                await bot.send_video(
                    chat_id=tg_id,
                    video=message.video.file_id,
                    caption=message.caption or ""
                )

            # Голосовое сообщение
            elif message.voice:
                await bot.send_voice(
                    chat_id=tg_id,
                    voice=message.voice.file_id,
                    caption=message.caption or ""
                )

            else:
                print("⚠️ Тип сообщения не поддержан:", message)

        except Exception as e:
            print(f"\n❌ Ошибка при отправке сообщения пользователю: {e}\n")


# Обработка сообщений от пользователя в БОТЕ
@router.message()
async def handle_message_from_user(message: Message):

    if message.text == '/broadcast':
        return

    user_topic = await UserTopics.get_by_tg_id(message.from_user.id)
    if not user_topic:
        await message.delete()
        return

    try:
        # Текст
        if message.text:
            await bot.send_message(
                chat_id=settings.bot.GROUP_ID,
                message_thread_id=user_topic.topic_id,
                text=message.text
            )

        # Фото
        elif message.photo:
            await bot.send_photo(
                chat_id=settings.bot.GROUP_ID,
                message_thread_id=user_topic.topic_id,
                photo=message.photo[-1].file_id,
                caption=message.caption or ""
            )

        # Документ
        elif message.document:
            await bot.send_document(
                chat_id=settings.bot.GROUP_ID,
                message_thread_id=user_topic.topic_id,
                document=message.document.file_id,
                caption=message.caption or ""
            )

        # Видео
        elif message.video:
            await bot.send_video(
                chat_id=settings.bot.GROUP_ID,
                message_thread_id=user_topic.topic_id,
                video=message.video.file_id,
                caption=message.caption or ""
            )

        # Голосовое сообщение
        elif message.voice:
            await bot.send_voice(
                chat_id=settings.bot.GROUP_ID,
                message_thread_id=user_topic.topic_id,
                voice=message.voice.file_id,
                caption=message.caption or ""
            )

        else:
            print("⚠️ Тип сообщения не поддержан:", message)

    except Exception as e:
        print(f"\n❌ Ошибка при отправке в топик: {e}\n")
