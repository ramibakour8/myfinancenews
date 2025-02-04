import yfinance as yf
import feedparser
from telegram import Bot
import schedule
import time

TOKEN = "8059510016:AAGex8esGI_d_Ch1XIZzso-B2FsuT1HCFvk"
CHANNEL_ID = "@ramibakourtrader"
bot = Bot(token=TOKEN)

# جلب بيانات الأسواق المالية
def get_market_updates():
    gold = yf.Ticker("GC=F").history(period="1d")["Close"].iloc[-1]  # الذهب
    oil = yf.Ticker("CL=F").history(period="1d")["Close"].iloc[-1]  # النفط
    dow_jones = yf.Ticker("^DJI").history(period="1d")["Close"].iloc[-1]  # داو جونز
    nasdaq = yf.Ticker("^IXIC").history(period="1d")["Close"].iloc[-1]  # ناسداك
    sp500 = yf.Ticker("^GSPC").history(period="1d")["Close"].iloc[-1]  # S&P 500

    message = f"""📊 تحديثات الأسواق المالية العالمية 📊
    
🟡 الذهب: ${gold:.2f} للأونصة
🛢 النفط: ${oil:.2f} للبرميل
📈 داو جونز: {dow_jones:.2f}
📉 ناسداك: {nasdaq:.2f}
📊 S&P 500: {sp500:.2f}

🔄 تحديث تلقائي يومي للأسواق المالية.
    """
    bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="Markdown")

# جلب أخبار بلومبيرغ
def get_bloomberg_news():
    feed_url = "https://www.bloomberg.com/feeds/podcasts/markets.xml"
    feed = feedparser.parse(feed_url)
    latest_news = feed.entries[:3]
    news_message = "📰 أحدث أخبار الأسواق من بلومبيرغ:\n\n"
    for news in latest_news:
        news_message += f"🔹 [{news.title}]({news.link})\n"
    bot.send_message(chat_id=CHANNEL_ID, text=news_message, parse_mode="Markdown")

# جلب أخبار رويترز
def get_reuters_news():
    feed_url = "https://www.reutersagency.com/feed/?best-topics=markets&post_type=best"
    feed = feedparser.parse(feed_url)
    latest_news = feed.entries[:3]
    news_message = "📰 أحدث أخبار الأسواق من رويترز:\n\n"
    for news in latest_news:
        news_message += f"🔹 [{news.title}]({news.link})\n"
    bot.send_message(chat_id=CHANNEL_ID, text=news_message, parse_mode="Markdown")

# جلب أخبار CNBC
def get_cnbc_news():
    feed_url = "https://www.cnbc.com/id/15839069/device/rss/rss.html"
    feed = feedparser.parse(feed_url)
    latest_news = feed.entries[:3]
    news_message = "📰 أحدث أخبار الأسواق من CNBC:\n\n"
    for news in latest_news:
        news_message += f"🔹 [{news.title}]({news.link})\n"
    bot.send_message(chat_id=CHANNEL_ID, text=news_message, parse_mode="Markdown")

# جدولة النشر اليومي
schedule.every().day.at("08:00").do(get_market_updates)
schedule.every().day.at("09:00").do(get_bloomberg_news)
schedule.every().day.at("10:00").do(get_reuters_news)
schedule.every().day.at("11:00").do(get_cnbc_news)

while True:
    schedule.run_pending()
    time.sleep(60)
