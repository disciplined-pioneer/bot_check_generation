from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="ℹ️ О нас", callback_data="info_about_us")],
        [InlineKeyboardButton(text="💰 Цены", callback_data="price_list")],
        [InlineKeyboardButton(text="✅ Оставить заявку", callback_data="submit_request")]
    ]
)
