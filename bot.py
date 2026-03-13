import requests
import time
import asyncio
from telegram import Bot

# --- زانیارییێن بوتێ تە ---
TOKEN = '8652574111:AAEAtgw9G-n5489pe0CST83bImdNK3fPs_c'
CHAT_ID = '8142540785' 
SYMBOL = 'BTCUSDT'
INTERVAL = '1h'

bot = Bot(token=TOKEN)

def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return 50  # Neutral if not enough data
    
    deltas = [prices[i+1] - prices[i] for i in range(len(prices)-1)]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    
    if avg_loss == 0: return 100
    
    for i in range(period, len(deltas)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        
    if avg_loss == 0: return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def get_data(symbol, interval):
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=100"
        res = requests.get(url).json()
        closes = [float(candle[4]) for candle in res]
        return closes
    except:
        return None

async def main():
    print("🚀 Prime_Vortex is starting (Lite Version)...")
    last_signal = None

    while True:
        try:
            prices = get_data(SYMBOL, INTERVAL)
            if prices:
                rsi = calculate_rsi(prices)
                price = prices[-1]
                print(f"Price: {price} | RSI: {rsi:.2f}")

                if rsi < 30 and last_signal != 'buy':
                    msg = f"🔵 **Prime_Vortex: BUY**\n💰 Price: ${price}\n📊 RSI: {rsi:.2f}"
                    await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode='Markdown')
                    last_signal = 'buy'
                elif rsi > 70 and last_signal != 'sell':
                    msg = f"🟠 **Prime_Vortex: SELL**\n💰 Price: ${price}\n📊 RSI: {rsi:.2f}"
                    await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode='Markdown')
                    last_signal = 'sell'
        except Exception as e:
            print(f"Error: {e}")
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
