import feedparser
import os
import json
import asyncio
from telegram import Bot
from telegram.request import HTTPXRequest

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@muhranews"
RSS_FEED = "https://muhraplatform.com/feed"
FILE_NAME = "posted.json"

request = HTTPXRequest(connect_timeout=30, read_timeout=30)
bot = Bot(token=TOKEN, request=request)

if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        posted_links = set(json.load(f))
else:
    posted_links = set()

async def send_news():
    feed = feedparser.parse(RSS_FEED)

    # oldest first, so Telegram order looks natural
    entries = list(feed.entries)
    entries.reverse()

    new_count = 0

    for entry in entries:
        link = entry.link

        if link not in posted_links:
            message = f"📰 {entry.title}\n\n{link}"

            await bot.send_message(
                chat_id=CHANNEL_ID,
                text=message
            )

            print("Posted:", entry.title)
            posted_links.add(link)
            new_count += 1

    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(list(posted_links), f, indent=2)

    print(f"Done. New posts: {new_count}")

asyncio.run(send_news())