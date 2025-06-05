import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, BotCommand
from dotenv import load_dotenv

from routers import main_router

load_dotenv()

TOKEN = os.getenv('TG_TOKEN')
storage = RedisStorage.from_url("redis://redis:6379")


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=storage)
    dp.include_router(main_router)

    commands = [
        BotCommand(command="/login", description="Войти в систему"),
        BotCommand(command="/register", description="Регистрация"),
        BotCommand(command="/send_photo", description="Отправить фото"),
    ]
    await bot.set_my_commands(commands)

    @dp.message(CommandStart())
    async def handle_start(msg: Message):
        await msg.answer("Добро пожаловать!")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
