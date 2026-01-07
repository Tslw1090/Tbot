import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("TG_SESSION")

BOT_CHAT_ID = int(os.getenv("BOT_CHAT_ID"))
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID"))

WATCH_CHATS = [
    -1003291372439
    -1003605900655
]

KEYWORDS = ["job", "hiring", "vacancy"]

client = TelegramClient(
    StringSession(SESSION),
    API_ID,
    API_HASH
)

@client.on(events.NewMessage(chats=WATCH_CHATS))
async def monitor(event):
    text = (event.text or "").lower()

    if any(k in text for k in KEYWORDS):
        await client.forward_messages(
            BOT_CHAT_ID,
            event.message
        )

@client.on(events.NewMessage(chats=BOT_CHAT_ID))
async def repost(event):
    await client.forward_messages(
        TARGET_CHAT_ID,
        event.message
    )

client.start()
client.run_until_disconnected()
