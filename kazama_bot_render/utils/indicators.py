
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

def calculate_ema(df, period):
    return df['Close'].ewm(span=period, adjust=False).mean()

def generate_chart(df, symbol):
    plt.figure(figsize=(10, 4))
    plt.plot(df['Close'], label='Precio', color='black')
    plt.plot(df['EMA20'], label='EMA 20', linestyle='--', color='blue')
    plt.plot(df['EMA50'], label='EMA 50', linestyle='--', color='red')
    plt.title(f"{symbol} - Señal")
    plt.legend()
    path = f"utils/chart_{symbol}.png"
    plt.savefig(path)
    plt.close()
    return path

def get_signal(symbol):
    end = datetime.now()
    start = end - timedelta(days=2)
    df = yf.download(symbol, start=start, end=end, interval='5m')
    if df.empty: return None

    df['EMA20'] = calculate_ema(df, 20)
    df['EMA50'] = calculate_ema(df, 50)
    df.dropna(inplace=True)

    last = df.iloc[-1]
    prev = df.iloc[-2]

    # Señal cruce EMA20 > EMA50
    if prev['EMA20'] < prev['EMA50'] and last['EMA20'] > last['EMA50']:
        entry = round(last['Close'], 2)
        tp = round(entry * 1.019, 2)
        sl = round(entry * 0.981, 2)
        image = generate_chart(df, symbol)
        return {
            "symbol": symbol,
            "entry": entry,
            "tp": tp,
            "sl": sl,
            "strategy": "Cruce EMA20/50",
            "image": image
        }
    return None
