from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from core.bot import bot
from bot.keyboards.start import *
from bot.templates.start import *

router = Router()

from test import create_topic

# Обработка входящих сообщений и "Назад" к старту
@router.message(Command("start", ignore_case=True))
@router.callback_query(F.data == "back_start")
async def cmd_start(message: Message | CallbackQuery, state: FSMContext):

    #await create_topic()

    # Удаляем всю историю сообщений
    data = await state.get_data()
    
    if isinstance(message, Message):
        report_id = data["report"] if 'report' in data else message.message_id - 90
        try:
            await bot.delete_messages(message.chat.id,
                                      list(range(max(1, message.message_id - 90, report_id + 1), message.message_id + 1)))
        except Exception:
            pass
        await message.answer(text=starting_message, reply_markup=start_keyboard)

    elif isinstance(message, CallbackQuery):
        # Если это CallbackQuery, то мы получаем сообщение через callback.message
        report_id = data["report"] if 'report' in data else message.message.message_id - 90
        try:
            await bot.delete_messages(message.message.chat.id,
                                      list(range(max(1, message.message.message_id - 90, report_id + 1), message.message.message_id + 1)))
        except Exception:
            pass
        await message.message.edit_text(text=starting_message, reply_markup=start_keyboard)