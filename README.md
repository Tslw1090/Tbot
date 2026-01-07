# Tbot

A simple Telegram bot that monitors specified chats for job-related keywords and forwards matching messages to a target chat.

## Features

- Monitors multiple Telegram chats for keywords like "job", "hiring", and "vacancy".
- Forwards matching messages to a designated bot chat.
- Automatically reposts messages from the bot chat to a target chat.

## Prerequisites

- Python 3.x
- A Telegram account
- API credentials from [Telegram API](https://my.telegram.org/)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Tslw1090/Tbot.git
   cd Tbot
   ```

2. Install dependencies:
   ```
   pip install telethon
   ```

## Configuration

Set the following environment variables:

- `API_ID`: Your Telegram API ID
- `API_HASH`: Your Telegram API Hash
- `TG_SESSION`: Your Telethon session string (generate using `key.py`)
- `BOT_CHAT_ID`: The chat ID where messages are initially forwarded
- `TARGET_CHAT_ID`: The final chat ID where messages are reposted

## Usage

Run the bot:
```
python main.py
```

The bot will start monitoring the specified chats and forward messages containing the keywords.

## License

This project is open-source. Feel free to use and modify.