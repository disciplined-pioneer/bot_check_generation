from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()

class BroadcastStates(StatesGroup):
    uploading_file = State()
    choosing_format = State()
    entering_caption = State()
    confirming = State()


@router.message(Command("broadcast"))
async def start_broadcast(message: types.Message, state: FSMContext):
    await message.answer("Отправь текст или файл для рассылки:")
    await state.set_state(BroadcastStates.uploading_file)


@router.message(BroadcastStates.uploading_file)
async def handle_universal_input(message: types.Message, state: FSMContext):
    data = {}

    if message.text:
        data = {"msg_type": "text", "content": message.text}
    elif message.photo:
        data = {"msg_type": "photo", "content": message.photo[-1].file_id}
    elif message.video:
        data = {"msg_type": "video", "content": message.video.file_id}
    elif message.audio:
        data = {"msg_type": "audio", "content": message.audio.file_id}
    elif message.document:
        data = {"msg_type": "document", "content": message.document.file_id}
    else:
        return await message.answer("Поддерживаются только текст, фото, видео, аудио и документы.")

    await state.update_data(**data)

    if data["msg_type"] == "text":
        await message.answer(
            "Выбери форматирование: Markdown или HTML",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="Markdown")], [KeyboardButton(text="HTML")]],
                resize_keyboard=True
            )
        )
        await state.set_state(BroadcastStates.choosing_format)
    else:
        await message.answer("Введи подпись (или '-' если без подписи):")
        await state.set_state(BroadcastStates.entering_caption)


@router.message(BroadcastStates.entering_caption)
async def handle_caption(message: types.Message, state: FSMContext):
    caption = None if message.text.strip() == '-' else message.text
    await state.update_data(caption=caption)

    await message.answer(
        "Выбери форматирование: Markdown или HTML",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Markdown")], [KeyboardButton(text="HTML")]],
            resize_keyboard=True
        )
    )
    await state.set_state(BroadcastStates.choosing_format)


@router.message(BroadcastStates.choosing_format)
async def handle_format_choice(message: types.Message, state: FSMContext):
    user_ids = []
    format_choice = message.text.strip().lower()
    if format_choice not in ["markdown", "html"]:
        return await message.answer("Выбери формат: Markdown или HTML")

    await state.update_data(parse_mode=format_choice.upper())
    data = await state.get_data()

    for user_id in user_ids:
        try:
            if data["msg_type"] == "text":
                await message.bot.send_message(
                    user_id,
                    data["content"],
                    parse_mode=data["parse_mode"]
                )
            elif data["msg_type"] == "photo":
                await message.bot.send_photo(
                    user_id,
                    data["content"],
                    caption=data.get("caption"),
                    parse_mode=data["parse_mode"]
                )
            elif data["msg_type"] == "video":
                await message.bot.send_video(
                    user_id,
                    data["content"],
                    caption=data.get("caption"),
                    parse_mode=data["parse_mode"]
                )
            elif data["msg_type"] == "audio":
                await message.bot.send_audio(
                    user_id,
                    data["content"],
                    caption=data.get("caption"),
                    parse_mode=data["parse_mode"]
                )
            elif data["msg_type"] == "document":
                await message.bot.send_document(
                    user_id,
                    data["content"],
                    caption=data.get("caption"),
                    parse_mode=data["parse_mode"]
                )
        except Exception as e:
            await message.answer(f"Ошибка при отправке пользователю {user_id}: {e}")

    await message.answer("Рассылка завершена.")
    await state.clear()