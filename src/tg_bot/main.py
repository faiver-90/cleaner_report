import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from dotenv import load_dotenv

from handlers import register, login

load_dotenv()

TOKEN = os.getenv('TG_TOKEN')


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(register.router)
    dp.include_router(login.router)

    @dp.message(CommandStart())
    async def handle_start(msg: Message):
        await msg.answer("Добро пожаловать!")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
