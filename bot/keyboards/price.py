from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

price_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Оставить заявку", callback_data="submit_request")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_start")]
    ]
)
