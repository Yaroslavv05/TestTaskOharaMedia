from telethon import TelegramClient, events
from models import get_engine, create_tables, get_session, Message

db_url = 'postgresql+psycopg2://user:password@database/db_name'
phone = ''
api_id = ''
api_hash = ''
client = TelegramClient('session_name', api_id, api_hash)

engine = get_engine('postgresql+psycopg2://user:password@database/db_name')
create_tables(engine)
session = get_session(engine)


@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.is_private:
        message_id = event.message.id
        text = event.message.message
        sender = await event.get_sender()
        first_name = sender.first_name
        last_name = sender.last_name
        username = sender.username
        phone_number = sender.phone
        date = event.message.date

        new_message = Message(
            message_id=message_id,
            text=text,
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone_number=phone_number,
            date=date
        )

        session.add(new_message)
        session.commit()

client.start(phone)
client.run_until_disconnected()
