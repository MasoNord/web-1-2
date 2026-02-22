from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from datetime import timedelta

from harmony_hound.adapters.redis.connection import redis_connection


class RecognitionRestrictionMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject,Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        print("Hello from Recognition Restriction Middleware")

        if event.video_note or event.voice or event.video:
            print("Checking active recognition processes for the current user")
            key = f"active_processing:{event.from_user.id}"

            async with redis_connection() as conn:
                is_locked = await conn.get(key)

                if is_locked is None:
                    return await handler(event, data)

                await event.answer(
                    "Sorry, but you have unfinished song recognition process...",
                    show_alert=True
                )

                return
        else:
            return await handler(event, data)