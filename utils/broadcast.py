import re
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Поиска всех ссылок в тексте
def extract_urls(text: str) -> list: 
    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, text)
    return urls


# Получение кнопок для обработки ссылок
def create_url_keyboard(text: str):
    urls = extract_urls(text)

    if not urls:
        return None

    # Формируем кнопки
    buttons = []
    if len(urls) == 1:
        buttons.append([InlineKeyboardButton(text="Ссылка", url=urls[0])])
    else:
        for i, url in enumerate(urls, 1):
            buttons.append([InlineKeyboardButton(text=f"Ссылка {i}", url=url)])
    
    # Возвращаем клавиатуру
    return InlineKeyboardMarkup(inline_keyboard=buttons)
