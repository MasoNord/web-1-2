
from aiogram import Router, F
from aiogram.types import Message
from datetime import timedelta
from harmony_hound.adapters.redis.connection import redis_connection
from harmony_hound.application.common.exceptions import FileSizeLimitError, FileDurationLimitError
from harmony_hound.main.config import bot
from harmony_hound.presentation.telegram.keyboards.main_keyboards import start_keyboard
from harmony_hound.presentation.telegram.services.abstract_processing_class import client_code
from aiogram.utils.chat_action import ChatActionSender
from harmony_hound.presentation.telegram.services.video_note_processing_class import VideoNoteProcessingClass
from harmony_hound.presentation.telegram.services.video_processing_class import VideoProcessingClass
from harmony_hound.presentation.telegram.services.voice_processing_class import VoiceProcessingClass

user_router = Router()

@user_router.message(F.text == "ℹ️ Info")
async def info (
        message: Message
):
    builder = start_keyboard(message)

    return await message.answer(
        "Hi, I'm Harmony Hound, and I can recognize songs, pretty cool, huh ?\n\n\
  What you can do:\n\
  \t\t 1. You can send me an audio/video file from your device\n\
  \t\t 2. Record a Telegram audio or video message in bottom\n\
  \t\t\t\t   right and capture music playing around you\n\n\
  Constraints:\n\
  \t\t 1. Minimal file duration accepted is 5 seconds\n\
  \t\t 2. Maximal file size is 100 Mb\n\
  \t\t 3. Optimal duration for uploaded file\n\
  \t\t\t\t   is 10-15 second (file with longer duration will be shorted)",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

@user_router.message(F.text == "💁‍♂️ Help")
async def help(
        message: Message
):
    builder = start_keyboard(message)

    return await message.answer(
        "Drop any audio file to the bot in the chat, "
        "wait for a couple of seconds, and enjoy your results!",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

@user_router.message(F.voice)
async def audio_processing(message: Message):
    key = f"active_processing:{message.from_user.id}"
    async with redis_connection() as conn:
        await conn.set(key, "True")
        try:
            async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
                response = await client_code(VoiceProcessingClass(), message)
        except FileSizeLimitError as e:
            await conn.delete(key)
            return await message.answer(str(e))
        except FileDurationLimitError as e:
            await conn.delete(key)
            return await message.answer(str(e))
        finally:
            await conn.delete(key)

    return await message.answer("Success!")

@user_router.message(F.video_note)
async def video_processing(message: Message):
    key = f"active_processing:{message.from_user.id}"

    async with redis_connection() as conn:
        await conn.set(key, "True")
        try:
            async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
                response = await client_code(VideoNoteProcessingClass(), message)
        except FileSizeLimitError as e:
            await conn.delete(key)
            return await message.answer(str(e))
        except FileDurationLimitError as e:
            await conn.delete(key)
            return await message.answer(str(e))
        finally:
            await conn.delete(key)

    return await message.answer("Success!")

@user_router.message(F.video)
async def video_file_processing(message: Message):
    key = f"active_processing:{message.from_user.id}"

    async with redis_connection() as conn:
        await conn.set(key, "True")
        try:
            async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
                response = await client_code(VideoProcessingClass(), message)
        except FileSizeLimitError as e:
            await conn.delete(key)
            return await message.answer(str(e))
        except FileDurationLimitError as e:
            await conn.delete(key)
            return await message.answer(str(e))
        finally:
            await conn.delete(key)

    return await message.answer("Success!")