import os
import re
import threading
from flask import Flask
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

PORT = int(os.getenv("PORT", 10000))  # Render provides PORT

WATCH_CHATS = [
    -1001111111111,
    -1002222222222,
    -1003333333333,
]

# -------------------------------------------------
# FLASK APP (Health Endpoint)
# -------------------------------------------------
app = Flask(__name__)

@app.route("/sutaa", methods=["GET", "POST"])
def sutaa():
    return "<h1>chalu hai</h1>"

def run_flask():
    app.run(host="0.0.0.0", port=PORT)

# -------------------------------------------------
# TELEGRAM CLIENT
# -------------------------------------------------
client = TelegramClient(
    StringSession(TG_SESSION),
    API_ID,
    API_HASH
)

URL_REGEX = re.compile(r"https?://|www\.", re.IGNORECASE)

def contains_url(message):
    if message.entities:
        for entity in message.entities:
            if isinstance(entity, (MessageEntityUrl, MessageEntityTextUrl)):
                return True

    if message.text and URL_REGEX.search(message.text):
        return True

    return False

# -------------------------------------------------
# 1️⃣ Monitor chats → forward to Bot A
# -------------------------------------------------
@client.on(events.NewMessage(chats=WATCH_CHATS))
async def forward_to_bot_a(event):
    if contains_url(event.message):
        await client.forward_messages(
            BOT_A_CHAT_ID,
            event.message
        )

# -------------------------------------------------
# 2️⃣ Monitor Bot A → forward to Bot B
# -------------------------------------------------
@client.on(events.NewMessage(chats=BOT_A_CHAT_ID))
async def forward_to_bot_b(event):
    await client.forward_messages(
        BOT_B_CHAT_ID,
        event.message
    )

# -------------------------------------------------
# START EVERYTHING
# -------------------------------------------------
if __name__ == "__main__":
    # Start Flask in background
    threading.Thread(target=run_flask, daemon=True).start()

    # Start Telegram client
    client.start()
    print("Telegram monitor started | /sutaa endpoint live")
    client.run_until_disconnected()
