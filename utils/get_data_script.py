import logging
from telethon import TelegramClient
from models import get_engine, create_tables, get_session, Message

logging.basicConfig(level=logging.INFO)

db_url = 'postgresql+psycopg2://user:password@database/db_name'
phone = ''
api_id = ''
api_hash = ''
session_name = 'session_name'

client = TelegramClient(session_name, api_id, api_hash)
engine = get_engine(db_url)
create_tables(engine)
session = get_session(engine)


async def mark_messages_as_read():
    async with client:
        await client.start(phone)

        async for dialog in client.iter_dialogs():
            if dialog.is_user and dialog.unread_count >= 1:
                async for message in client.iter_messages(dialog.id, limit=dialog.unread_count):
                    sender = await message.get_sender()

                    logging.info(f'Message ID: {message.id}')
                    logging.info(f'Text: {message.message}')
                    logging.info(f'Sender: {sender.first_name} {sender.last_name} (@{sender.username})')
                    logging.info(f'Phone number: {sender.phone}')
                    logging.info(f'Date: {message.date}')

                    await client.send_read_acknowledge(dialog.id, message)

                    new_message = Message(
                        message_id=message.id,
                        text=message.message,
                        first_name=sender.first_name,
                        last_name=sender.last_name,
                        username=sender.username,
                        phone_number=sender.phone,
                        date=message.date
                    )
                    session.add(new_message)
                    session.commit()

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(mark_messages_as_read())
