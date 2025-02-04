import yfinance as yf
import asyncio
from telegram import Bot

TOKEN = "8059510016:AAGex8esGI_d_Ch1XIZzso-B2FsuT1HCFvk"
CHANNEL_ID = "@ramibakourtrader"

bot = Bot(token=TOKEN)

# وظيفة لجلب سعر الذهب
def get_gold_price():
    gold = yf.Ticker("GC=F")
    data = gold.history(period="1d")
    return f"📊 سعر الذهب اليوم: {data['Close'][0]:.2f} دولار للأونصة"

# وظيفة لجلب سعر النفط
def get_oil_price():
    oil = yf.Ticker("CL=F")
    data = oil.history(period="1d")
    return f"🛢️ سعر النفط اليوم: {data['Close'][0]:.2f} دولار للبرميل"

# وظيفة لجلب بيانات مؤشر S&P 500
def get_sp500():
    sp500 = yf.Ticker("^GSPC")
    data = sp500.history(period="1d")
    return f"📉 مؤشر S&P 500 اليوم: {data['Close'][0]:.2f}"

# وظيفة لجلب بيانات مؤشر Dow Jones
def get_dow_jones():
    dow = yf.Ticker("^DJI")
    data = dow.history(period="1d")
    return f"📊 مؤشر داو جونز اليوم: {data['Close'][0]:.2f}"

# وظيفة لإرسال رسالة مع معالجة الأخطاء
async def send_auto_message(message):
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=message)
        print("✅ تم إرسال الخبر الاقتصادي بنجاح!")
    except Exception as e:
        print(f"❌ فشل في إرسال الرسالة: {e}")

# جلب البيانات الاقتصادية المتنوعة
economic_news = (
    get_gold_price() + "\n" +
    get_oil_price() + "\n" +
    get_sp500() + "\n" +
    get_dow_jones()
)

# إرسال الرسالة فورًا
asyncio.run(send_auto_message(economic_news))
