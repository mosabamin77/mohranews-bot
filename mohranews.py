import feedparser
import os
import json
import asyncio
from telegram import Bot
from telegram.request import HTTPXRequest

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@muhranews"
RSS_FEED = "https://muhraplatform.com/feed"

request = HTTPXRequest(
    connect_timeout=30,
    read_timeout=30
)

bot = Bot(token=TOKEN, request=request)

FILE_NAME = "posted.json"

if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r") as f:
        posted_links = set(json.load(f))
else:
    posted_links = set()

async def send_news():

    feed = feedparser.parse(RSS_FEED)

    for entry in feed.entries:

        if entry.link not in posted_links:

            message = f"""
📰 {entry.title}

{entry.link}
"""

            await bot.send_message(
                chat_id=CHANNEL_ID,
                text=message
            )

            print("Posted:", entry.title)

            posted_links.add(entry.link)

    with open(FILE_NAME, "w") as f:
        json.dump(list(posted_links), f)

asyncio.run(send_news())