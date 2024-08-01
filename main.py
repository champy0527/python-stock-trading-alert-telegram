import asyncio
from stock import Stock
from news import News
from telegram import Bot
import os
from dotenv import load_dotenv

load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "Tesla"

stock_api_key = os.getenv("STOCK_API_KEY")
news_api_key = os.getenv("NEWS_API_KEY")

BOT_TOKEN = os.getenv("TLGRM_BOT_TOKEN")
bot_chat_id = os.getenv("TLGRM_CHAT_ID")

stock = Stock(STOCK, stock_api_key)
news = News(COMPANY_NAME.lower(), news_api_key)

async def telegram_bot_sendtext(bot_message):
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=bot_chat_id, text=bot_message)

async def main():
    direction = stock.up_or_down()
    percentage_change = stock.get_closing_percentage_change()
    if stock.is_5percent_change():
        for headline, brief in news.zip_article_dict().items():
            await telegram_bot_sendtext(
                f"{STOCK}: {direction}{percentage_change}%"
                f"\nHeadline: {headline}"
                f"\nBrief: {brief}"
            )
    else:
        for headline, brief in news.zip_article_dict().items():
            await telegram_bot_sendtext(
                f"{STOCK}: {direction}{percentage_change}%"
                f"\n\nHEADLINE: {headline}"
                f"\nBRIEF: {brief}"
            )

if __name__ == "__main__":
    asyncio.run(main())
