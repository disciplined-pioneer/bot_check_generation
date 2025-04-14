from aiogram import Router, F, types

from utils.submit_request import *
from bot.templates.submit_request import *

router = Router()

# Обрабатываем "Оставить заявку"
@router.callback_query(F.data == "submit_request")
async def show_price_list(callback: types.CallbackQuery):

    # Если нет заявки
    result = True
    if not result:
        await callback.message.edit_text(
            text=already_sent_message,
            reply_markup=None
        )
        return
    
    # Сообщение пользователю
    topic_id = await create_topic(callback.from_user)
    await callback.message.edit_text(
        text=success_message,
        reply_markup=None
    )

    await callback.answer()