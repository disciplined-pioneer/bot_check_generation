from aiogram import Router, F, types

from bot.templates.price import *
from bot.keyboards.price import *

router = Router()

# Обрабатываем "Цены"
@router.callback_query(F.data == "price_list")
async def show_price_list(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=price_info_text,
        reply_markup=price_keyboard
    )
    await callback.answer()