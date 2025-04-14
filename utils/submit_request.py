from core.bot import bot
from settings import settings
from aiogram.types import ForumTopic


# Создание топика
async def create_topic(topic_name: str) -> int:

    topic: ForumTopic = await bot.create_forum_topic(
        chat_id=settings.bot.GROUP_ID,
        name=topic_name
    )

    print("\n\nСоздан топик:", topic.name)
    print(f"ID топика (message_thread_id): {topic.message_thread_id}\n\n")

    # Тут мы должны добавить данные в таблицу

    return topic.message_thread_id