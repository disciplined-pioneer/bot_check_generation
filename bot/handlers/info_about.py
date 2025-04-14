from aiogram import Router, F, types

from bot.templates.info_about import *
from bot.keyboards.info_about import *

router = Router()

# Обрабатываем "О нас"
@router.callback_query(F.data == "info_about_us")
async def show_price_list(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=info_about_text,
        reply_markup=info_about_keyboard
    )
    await callback.answer()