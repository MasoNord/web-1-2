
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

recognition_router = Router()

@recognition_router.message(F.voice)
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

@recognition_router.message(F.video_note)
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

@recognition_router.message(F.video)
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