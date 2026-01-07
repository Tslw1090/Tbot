import os
import re
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import MessageEntityUrl, MessageEntityTextUrl

# -------------------------------------------------
# ENV VARIABLES
# -------------------------------------------------
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
TG_SESSION = os.getenv("TG_SESSION")

BOT_A_CHAT_ID = int(os.getenv("BOT_A_CHAT_ID"))
BOT_B_CHAT_ID = int(os.getenv("BOT_B_CHAT_ID"))

# Chats (groups / channels) to monitor
WATCH_CHATS = [
    -1001111111111,
    -1002222222222,
    -1003333333333,
]

# -------------------------------------------------
# INIT CLIENT
# -------------------------------------------------
client = TelegramClient(
    StringSession(TG_SESSION),
    API_ID,
    API_HASH
)

# -------------------------------------------------
# URL DETECTION (ENTITY + REGEX)
# -------------------------------------------------
URL_REGEX = re.compile(r"https?://|www\.", re.IGNORECASE)

def contains_url(message):
    # Check Telegram-parsed entities (best method)
    if message.entities:
        for entity in message.entities:
            if isinstance(entity, (MessageEntityUrl, MessageEntityTextUrl)):
                return True

    # Fallback regex check
    if message.text and URL_REGEX.search(message.text):
        return True

    return False

# -------------------------------------------------
# 1️⃣ Monitor multiple chats → forward to Bot A
# -------------------------------------------------
@client.on(events.NewMessage(chats=WATCH_CHATS))
async def forward_to_bot_a(event):
    try:
        if contains_url(event.message):
            await client.forward_messages(
                BOT_A_CHAT_ID,
                event.message
            )
    except Exception as e:
        print("Error forwarding to Bot A:", e)

# -------------------------------------------------
# 2️⃣ Monitor Bot A → forward to Bot B
# -------------------------------------------------
@client.on(events.NewMessage(chats=BOT_A_CHAT_ID))
async def forward_to_bot_b(event):
    try:
        await client.forward_messages(
            BOT_B_CHAT_ID,
            event.message
        )
    except Exception as e:
        print("Error forwarding to Bot B:", e)

# -------------------------------------------------
# START CLIENT
# -------------------------------------------------
client.start()
print("Telegram monitor started...")
client.run_until_disconnected()
