from telethon import TelegramClient
from telethon.sessions import StringSession

api_id = 3886268
api_hash = "15cd8079fc1f902c8fb3c0b6dae1ed5"

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print(client.session.save())
