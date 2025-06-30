import os
import time
import telebot
from utils.indicators import get_signal

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = telebot.TeleBot(TOKEN)

symbols = ["BTCUSDT", "ETHUSDT", "^NDX", "^GSPC", "^GDAXI"]

def send_signal(signal):
    if not signal: return
    image_path = signal["image"]
    message = f'''
🚨 Señal detectada - {signal["symbol"]}
📍 Estrategia: {signal["strategy"]}
🎯 Entrada: {signal["entry"]}
✅ TP: {signal["tp"]}
❌ SL: {signal["sl"]}
⏱ Timeframe: 5m
    '''.strip()
    with open(image_path, "rb") as photo:
        bot.send_photo(CHAT_ID, photo, caption=message)

if __name__ == "__main__":
    while True:
        for symbol in symbols:
            signal = get_signal(symbol)
            send_signal(signal)
            time.sleep(5)
        time.sleep(300)