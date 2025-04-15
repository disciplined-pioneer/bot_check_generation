from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def format_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Markdown", callback_data="format_markdown")],
            [InlineKeyboardButton(text="HTML", callback_data="format_html")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
        ]
    )

cancel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
    ]
)