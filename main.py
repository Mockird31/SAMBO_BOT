import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
import os

from app.handlers import router

from find_athete import get_info

TOKEN = os.getenv("TOKEN_SAMBO")

logging.basicConfig(level=logging.INFO)

bot = Bot(TOKEN)
dp = Dispatcher()
    

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())