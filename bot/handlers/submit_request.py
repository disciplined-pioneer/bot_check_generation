from aiogram import Router, F, types
from db.models.models import UserTopics

from utils.submit_request import *
from bot.templates.submit_request import *


router = Router()


# Обрабатываем "Оставить заявку"
@router.callback_query(F.data == "submit_request")
async def show_price_list(callback: types.CallbackQuery):

    # Если нет заявки
    result = await UserTopics.get_by_tg_id(callback.from_user.id)
    if not result:
        topic_id = await create_topic(callback.from_user)
        await callback.message.edit_text(
            text=success_message,
            reply_markup=None
        )
        return
    
    # Если есть заявка
    await callback.message.edit_text(
        text=already_sent_message,
        reply_markup=None
    )

    await callback.answer()