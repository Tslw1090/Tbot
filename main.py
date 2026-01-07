import os
import re
import asyncio
from datetime import datetime
from fastapi import FastAPI
import uvicorn
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import MessageEntityUrl, MessageEntityTextUrl

# --------------------------
# ENV VARIABLES
# --------------------------
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
TG_SESSION = os.getenv("TG_SESSION")

BOT_A_CHAT_ID = int(os.getenv("BOT_A_CHAT_ID"))
BOT_B_CHAT_ID = int(os.getenv("BOT_B_CHAT_ID"))

# Chats (groups/channels) to monitor
WATCH_CHATS = [
    -1003503245562,
    -1003291372439,
    -1003605900655,
]

# Port for FastAPI (Render sets this automatically)
PORT = int(os.getenv("PORT", 10000))

# --------------------------
# URL DETECTION FUNCTION
# --------------------------
URL_REGEX = re.compile(r"https?://|www\.", re.IGNORECASE)

def contains_url(message):
    """Return True if message contains any URL"""
    if message.entities:
        for entity in message.entities:
            if isinstance(entity, (MessageEntityUrl, MessageEntityTextUrl)):
                return True
    if message.text and URL_REGEX.search(message.text):
        return True
    return False

# --------------------------
# TELEGRAM CLIENT SETUP
# --------------------------
client = TelegramClient(StringSession(TG_SESSION), API_ID, API_HASH)

# --------------------------
# FASTAPI HEALTH ENDPOINT
# --------------------------
app = FastAPI()

@app.get("/sutaa")
@app.post("/sutaa")
async def sutaa():
    return {"status": "chalu hai"}

# --------------------------
# HELPER FUNCTION TO LOG
# --------------------------
def log_message(prefix, event):
    chat_name = getattr(event.chat, 'title', str(event.chat_id))
    sender_name = getattr(event.sender, 'first_name', 'Unknown')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text_preview = (event.text or "").replace("\n", " ")[:100]
    print(f"[{timestamp}] {prefix} | Chat: {chat_name} | Sender: {sender_name} | Text: {text_preview}", flush=True)

# --------------------------
# 1️⃣ MONITOR MULTIPLE CHATS → FORWARD TO BOT A
# --------------------------
@client.on(events.NewMessage(chats=WATCH_CHATS))
async def forward_to_bot_a(event):
    try:
        if contains_url(event.message):
            await client.forward_messages(BOT_A_CHAT_ID, event.message)
            log_message("Forwarded to Bot A", event)
    except Exception as e:
        print(f"Error forwarding to Bot A: {e}", flush=True)

# --------------------------
# 2️⃣ MONITOR BOT A → FORWARD TO BOT B
# --------------------------
@client.on(events.NewMessage(chats=BOT_A_CHAT_ID))
async def forward_to_bot_b(event):
    try:
        # ❌ Ignore messages sent by YOU
        if event.out:
            return

        # ✅ Forward only messages NOT sent by you
        await client.forward_messages(
            BOT_B_ENTITY,
            event.message
        )
        log_message("Forwarded to Bot B", event)

    except Exception as e:
        print(f"Error forwarding to Bot B: {e}", flush=True)

# --------------------------
# START TELEGRAM CLIENT + FASTAPI
# --------------------------
if __name__ == "__main__":
    async def main():
        await client.start()
        print("Telegram monitor started... | /sutaa endpoint live", flush=True)
        # Run FastAPI + Telethon concurrently
        config = uvicorn.Config(app, host="0.0.0.0", port=PORT, log_level="info")
        server = uvicorn.Server(config)
        await asyncio.gather(server.serve(), client.run_until_disconnected())

    asyncio.run(main())
