import asyncio
from telegram import Bot

TOKEN = "8059510016:AAEYLx7rY04Fo6QvBwlQFNO4hOLllYLHuIk"
CHANNEL_ID = "@ramibakourforex"  # استخدم المعرف الصحيح للقناة

bot = Bot(token=TOKEN)

async def send_message():
    # إرسال رسالة تجريبية
    await bot.send_message(chat_id=CHANNEL_ID, text="✅ اختبار: هل يعمل البوت في القناة؟")
    print("✅ تم إرسال الرسالة بنجاح!")  # تأكيد الإرسال في الـ Terminal

# تشغيل المهمة غير المتزامنة
asyncio.run(send_message())
