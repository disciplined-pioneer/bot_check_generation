from aiogram import Router, F, types
from bot.templates.submit_request import *

router = Router()

# Обрабатываем "Оставить заявку"
@router.callback_query(F.data == "submit_request")
async def show_price_list(callback: types.CallbackQuery):

    # Тут мы должны проверить на наличие заявки
    result = False
    if not result:
        await callback.message.edit_text(
            text=already_sent_message,
            reply_markup=None
        )
        return
        
    await callback.message.edit_text(
        text=success_message,
        reply_markup=None
    )
    await callback.answer()