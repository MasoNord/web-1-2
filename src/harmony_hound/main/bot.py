import asyncio
import logging

from logging import getLogger

from harmony_hound.presentation.telegram.middleware.recognition_restriction_middleware import \
    RecognitionRestrictionMiddleware
from src.harmony_hound.presentation.telegram.routers.user import user_router
from src.harmony_hound.main.config import bot, dp, admins
from aiogram.types import BotCommand, BotCommandScopeDefault
from src.harmony_hound.presentation.telegram.routers.start import start_router
from harmony_hound.presentation.telegram.routers.storage import storage_router

logger = getLogger(__name__)

async def set_commands():
    commands = [BotCommand(command='start', description='Старт')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

async def start_bot():
    await set_commands()

    try:
        await bot.send_message(f'I\'m running 🥳')
    except:
        pass

    logging.info("Bot is running successfully!")

async def stop_bot():

    await bot.send_message('The bot has been stop! Why?😔')

    await bot.session.close()

    logging.info("The bot has been stop successfully!")


async def main():
    dp.include_router(start_router)
    dp.include_router(user_router)
    dp.include_router(storage_router)

    user_router.message.middleware(RecognitionRestrictionMiddleware())
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())

