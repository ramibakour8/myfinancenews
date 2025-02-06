import yfinance as yf

# تحميل بيانات الذهب
gold = yf.Ticker("GC=F")

# استخراج السعر الحالي
gold_price = gold.history(period="1d")['Close'].iloc[-1]

print(f"💰 سعر الذهب الآن: {gold_price} دولار للأوقية.")
