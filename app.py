from flask import Flask, request
import json
import requests

app = Flask(__name__)

TOKEN = '8059510016:AAGex8esGI_d_Ch1XIZzso-B2FsuT1HCFvk'
WEBHOOK_URL = f'https://api.telegram.org/bot{TOKEN}/setWebhook'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    chat_id = data['message']['chat']['id']
    text = "تم استلام الرسالة!"
    
    # أرسل ردًا إلى Telegram
    requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', json={
        'chat_id': chat_id,
        'text': text
    })
    
    return 'OK', 200

if __name__ == '__main__':
    app.run(debug=True)
