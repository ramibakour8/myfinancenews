import time
import schedule
import asyncio
from telegram import Bot

TOKEN = "8059510016:AAEYLx7rY04Fo6QvBwlQFNO4hOLllYLHuIk"
CHANNEL_ID = "@ramibakourtrader"

bot = Bot(token=TOKEN)

async def send_auto_message():
    await bot.send_message(chat_id=CHANNEL_ID, text="📢 تحديث اقتصادي جديد!")

def job():
    asyncio.run(send_auto_message())

# جدولة نشر الأخبار كل ساعة
schedule.every(1).hours.do(job)

print("✅ البوت يعمل وسيقوم بنشر الأخبار كل ساعة...")

while True:
    schedule.run_pending()
    time.sleep(60)  # انتظار 60 ثانية قبل التحقق مرة أخرى
