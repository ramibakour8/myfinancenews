import requests
import asyncio
from telegram import Bot

# إعداد مفتاح API من NewsAPI
NEWS_API_KEY = '42055e99cb0149b7b74fe7a210078d4d'  # استبدل هذا بمفتاحك الفعلي
NEWS_API_URL = 'https://newsapi.org/v2/top-headlines'

# إعداد التوكن والمعرف
TOKEN = "8059510016:AAGex8esGI_d_Ch1XIZzso-B2FsuT1HCFvk"
CHANNEL_ID = "ramibakourtrader"
bot = Bot(token=TOKEN)

# دالة لجلب سعر الذهب
def get_gold_price():
    # استبدل هذا بكود جلب سعر الذهب من مصدر موثوق (مثل yfinance أو API آخر)
    return "💰 سعر الذهب اليوم: 1825.50 دولارًا للأونصة"

# دالة لجلب سعر النفط
def get_oil_price():
    # استبدل هذا بكود جلب سعر النفط
    return "⛽️ سعر النفط اليوم: 72.35 دولارًا للبرميل"

# دالة لجلب أخبار اقتصادية
def get_economic_news():
    params = {
        'apiKey': NEWS_API_KEY,
        'category': 'business',  # فئة الأعمال
        'language': 'ar',         # اللغة العربية
        'pageSize': 5             # عدد الأخبار
    }
    response = requests.get(NEWS_API_URL, params=params)
    if response.status_code == 200:
        articles = response.json()['articles']
        news = "📰 أهم الأخبار الاقتصادية العاجلة:\n"
        for article in articles:
            title = article['title']
            url = article['url']
            news += f"📌 {title}\n{url}\n\n"
        return news
    else:
        return "❌ فشل في جلب الأخبار العاجلة"

# دالة لإرسال رسالة تلقائيًا
async def send_auto_message(message):
    await bot.send_message(chat_id=CHANNEL_ID, text=message)

# دمج الأخبار الاقتصادية مع أسعار الأصول المالية
def send_combined_message():
    economic_news = (
        get_gold_price() + "\n" +
        get_oil_price() + "\n" +
        get_economic_news()  # إضافة الأخبار الاقتصادية العاجلة
    )
    # إرسال الرسالة
    asyncio.run(send_auto_message(economic_news))

# إرسال الرسالة فورًا
send_combined_message()
