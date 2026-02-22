from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types

def start_keyboard(message: types.Message):
    builder = ReplyKeyboardBuilder()

    builder.add(types.KeyboardButton(text="ℹ️ Info"))
    builder.add(types.KeyboardButton(text="💁‍♂️ Help"))
    builder.add(types.KeyboardButton(text=str("🗂️ Collected Data")))

    builder.adjust(4)

    return builder
