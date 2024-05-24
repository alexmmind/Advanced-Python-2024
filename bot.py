from handlers.view_statistics import view_statistics
from handlers import help, start, start_bot, reminder
from handlers.create_note import create_note
from handlers.find_note import find_note
from modules.config_reader import config
from aiogram import Bot, Dispatcher
import asyncio
import logging

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="None")
    dp = Dispatcher()
    dp.include_routers(start.router, start_bot.router, help.router, create_note.router, find_note.router, view_statistics.router, reminder.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())