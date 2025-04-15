import re
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Поиска всех ссылок в тексте
def extract_urls(text: str) -> list: 
    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, text)
    return urls


# Удаляем все http/https ссылки
def remove_urls(text: str) -> str:
    
    url_pattern = r'https?://[^\s,]+'
    cleaned_text = re.sub(url_pattern, '', text)
    
    # Удаляем лишние пробелы и запятые, если они остались после удаления
    cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text)  # двойные пробелы
    cleaned_text = re.sub(r'\s+,', ',', cleaned_text)    # пробел перед запятой
    cleaned_text = re.sub(r',\s+', ', ', cleaned_text)   # нормализация запятых
    return cleaned_text.strip()


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
