from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from settings import settings
from bot.keyboards.admin.broadcast import *
from bot.templates.admin.broadcast import *
from db.models.models import UserTopics
from utils.broadcast import create_url_keyboard, remove_urls


router = Router()


# Обрабатываем команду по рассылке сообщени
@router.message(Command("broadcast"))
async def start_broadcast(message: types.Message, state: FSMContext):

    # Если это не админ
    await message.delete()
    if message.from_user.id not in settings.bot.ADMINS:
        
        await message.answer(access_denied_message)
        await state.clear()
        return
    
    # Если админ
    sent = await message.answer(broadcast_prompt_message,
                                reply_markup=cancel_keyboard)
    await state.update_data(last_bot_message_id=sent.message_id)
    await state.set_state(BroadcastStates.uploading_file)
    

# Обрабатываем полученные данные от админа
@router.message(BroadcastStates.uploading_file)
async def handle_universal_input(message: types.Message, state: FSMContext):
    await message.delete()
    msg_data = {}

    # Тип сообщения
    if message.text:
        msg_data = {"msg_type": "text", "content": message.text}
    elif message.photo:
        msg_data = {"msg_type": "photo", "content": message.photo[-1].file_id}
    elif message.video:
        msg_data = {"msg_type": "video", "content": message.video.file_id}
    elif message.audio:
        msg_data = {"msg_type": "audio", "content": message.audio.file_id}
    elif message.document:
        msg_data = {"msg_type": "document", "content": message.document.file_id}
    else:
        return

    await state.update_data(**msg_data)
    data = await state.get_data()
    msg_id = data.get("last_bot_message_id")

    if msg_data["msg_type"] == "text":
        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=msg_id,
            text=choose_format_message,
            reply_markup=format_keyboard()
        )
        await state.set_state(BroadcastStates.choosing_format)
    else:
        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=msg_id,
            text=enter_caption_message,
            reply_markup=cancel_keyboard
        )
        await state.set_state(BroadcastStates.entering_caption)


# Выбираем тип форматирования
@router.message(BroadcastStates.entering_caption)
async def handle_caption(message: types.Message, state: FSMContext):
    await message.delete()
    caption = None if message.text.strip() == '-' else message.text
    await state.update_data(caption=caption)

    data = await state.get_data()
    msg_id = data.get("last_bot_message_id")

    await message.bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=msg_id,
        text=choose_format_message,
        reply_markup=format_keyboard()
    )
    await state.set_state(BroadcastStates.choosing_format)


# Обработка форматирования и отправка сообщений
@router.callback_query(lambda c: c.data.startswith("format_"))
async def handle_format_choice(callback: types.CallbackQuery, state: FSMContext):
    format_choice = callback.data.split("_")[1]

    await state.update_data(parse_mode=format_choice.upper())
    data = await state.get_data()

    user_topics = await UserTopics.all()
    user_ids = [u.tg_id for u in user_topics]

    for user_id in user_ids:
        try:
            if data["msg_type"] == "text":
                await callback.bot.send_message(user_id,
                                                remove_urls(data["content"]),
                                                parse_mode=data["parse_mode"],
                                                reply_markup=create_url_keyboard(data['content']))
            elif data["msg_type"] == "photo":
                await callback.bot.send_photo(user_id, data["content"],
                                              caption=remove_urls(data.get("caption")),
                                              parse_mode=data["parse_mode"],
                                              reply_markup=create_url_keyboard(data.get("caption")))
            elif data["msg_type"] == "video":
                await callback.bot.send_video(user_id, data["content"],
                                              caption=remove_urls(data.get("caption")),
                                              parse_mode=data["parse_mode"],
                                              reply_markup=create_url_keyboard(data.get("caption")))
            elif data["msg_type"] == "audio":
                await callback.bot.send_audio(user_id,
                                              data["content"],
                                              caption=remove_urls(data.get("caption")),
                                              parse_mode=data["parse_mode"],
                                              reply_markup=create_url_keyboard(data.get("caption")))
            elif data["msg_type"] == "document":
                await callback.bot.send_document(user_id,
                                                 data["content"],
                                                 caption=remove_urls(data.get("caption")),
                                                 parse_mode=data["parse_mode"],
                                                 reply_markup=create_url_keyboard(data.get("caption")))
        except Exception as e:
            print(f"Ошибка при отправке пользователю {user_id}: {e}")

    # Редактируем сообщение на новое
    msg_id = data.get("last_bot_message_id")
    await callback.bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=msg_id,
        text=broadcast_complete_message,
        reply_markup=None
    )
    await callback.answer()
    await state.clear()


# Обработка кнопки "Отмена"
@router.callback_query(lambda c: c.data == "cancel")
async def handle_cancel(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get("last_bot_message_id")

    await callback.bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=msg_id,
        text=broadcast_cancelled_message,
        reply_markup=None
    )
    await callback.answer()
    await state.clear()