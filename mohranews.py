import asyncio
import feedparser
from telegram import Bot
from telegram.request import HTTPXRequest
import os

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@muhranews"
RSS_FEED = "https://muhraplatform.com/feed"

request = HTTPXRequest(
    connect_timeout=30,
    read_timeout=30
)

bot = Bot(
    token=TOKEN,
    request=request
)

posted_links = set()

async def send_news():
    while True:
        try:
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

            await asyncio.sleep(60)

        except Exception as e:
            print("Error:", e)
            await asyncio.sleep(10)

asyncio.run(send_news())