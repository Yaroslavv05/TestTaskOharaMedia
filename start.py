import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from utils.models import get_engine, get_session, get_all_messages

dp = Dispatcher()

TOKEN = '7079282317:AAGUX4cOs43GoEVrkr-JGvxpK1A76mf_X-0'
db_url = 'postgresql+psycopg2://user:password@database/db_name'


@dp.message(CommandStart())
async def handle_start(message: Message) -> None:
    """Handle the /start command."""
    await message.answer(
        f"Hi {message.from_user.full_name}, this bot is for a test job from Ohara Media. "
        f"I can send you the last 10 records in the database. To do so, run this /latest command 😉"
    )


@dp.message(Command('latest'))
async def handle_latest(message: Message) -> None:
    """Handle the /latest command and return the last 10 messages from the database."""
    engine = get_engine(db_url)
    session = get_session(engine)

    messages = get_all_messages(session)
    response = "\n".join(
        f"ID: {msg.message_id}\n"
        f"First Name: {msg.first_name}\n"
        f"Last Name: {msg.last_name}\n"
        f"Username: {msg.username}\n"
        f"Message: {msg.text}\n"
        f"Received at: {msg.date}\n"
        for msg in messages[-10:]
    )
    await message.answer(response if response else "No messages found.")


async def main() -> None:
    """Main entry point for the bot."""
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
