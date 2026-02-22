from aiogram import Router, F
from aiogram.types import Message

storage_router = Router()

@storage_router.message(F.text == "Add song")
async def add_song_to_liked(message: Message):
    pass

@storage_router.message(F.text == "Get songs")
async def get_liked_songs(message: Message):
    pass

@storage_router.messsage(F.text == "Get song")
async def get_liked_song(message: Message):
    pass

@storage_router.message(F.text == "Remove linked")
async def remove_from_linked_songs(message: Message):
    pass