from aiogram import Router, F
from aiogram.filters.command import Command
from harmony_hound.presentation.telegram.keyboards.main_keyboards import start_keyboard
from aiogram.types import Message

help_router = Router()

@help_router.message(F.text == "💁‍♂️ Help")
async def help(
        message: Message
):
    builder = start_keyboard(message)

    return await message.answer(
        "Drop any audio file to the bot in the chat, "
        "wait for a couple of seconds, and enjoy your results!",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )