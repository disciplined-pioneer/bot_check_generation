from core.bot import bot
from settings import settings
from aiogram.types import ForumTopic


# Создание топика
async def create_topic(user: str) -> int:

    # Выбираем имя для топика
    if user.username:
        topic_name = f"@{user.username}"
    else:
        topic_name = user.first_name

    topic: ForumTopic = await bot.create_forum_topic(
        chat_id=settings.bot.GROUP_ID,
        name=topic_name
    )

    topic_id = topic.message_thread_id
    print("\n\nСоздан топик:", topic.name)
    print(f"ID топика (message_thread_id): {topic_id}\n\n")

    # Сообщение админу
    await bot.send_message(
        chat_id=settings.bot.GROUP_ID,
        text=f"Пользователь: {topic.name}\nID: {user.id}\n❗️ Оставил новую заявку",
        message_thread_id=topic_id
    )

    # Тут мы должны добавить данные в таблицу

    return topic_id