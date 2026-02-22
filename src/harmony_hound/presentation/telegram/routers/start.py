from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message

from src.harmony_hound.presentation.telegram.keyboards.main_keyboards import start_keyboard

start_router = Router()

@start_router.message(Command("start"))
async def start(
        message: Message
):
    builder = start_keyboard(message)

    return await message.answer(
        "Welcome to Harmony Hound 🥳\n"
        "Telegram bot which can guess any song you want to know about 💪",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )


