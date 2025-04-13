import asyncio
from db.crud.base import init_postgres

from db.models.models import UserTopics


async def main():
    await init_postgres()
    new_user = await UserTopics.create(tg_id=123589,  # Telegram ID пользователя
                    thread_id=1001,   # ID топика
                    username="user123",  # Имя пользователя (если есть)
                    )
    print(new_user.id)

asyncio.run(main())