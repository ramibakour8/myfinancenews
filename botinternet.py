import requests

try:
    response = requests.get("https://www.google.com", timeout=5)
    print("✅ الاتصال بالإنترنت ناجح!")
except requests.ConnectionError:
    print("❌ لا يوجد اتصال بالإنترنت! تحقق من الشبكة.")
