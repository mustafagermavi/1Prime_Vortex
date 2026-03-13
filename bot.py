import requests
import pandas as pd
import pandas_ta as ta
import time
import asyncio
from telegram import Bot

# --- زانیارییێن تە یێن جێگیر ---
TOKEN = '8652574111:AAEAtgw9G-n5489pe0CST83bImdNK3fPs_c'
CHAT_ID = '8142540785' # ئایدییا تە یێ تایبەت
SYMBOL = 'BTCUSDT'
INTERVAL = '1h'

bot = Bot(token=TOKEN)

def get_data(symbol, interval):
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=100"
        res = requests.get(url).json()
        df = pd.DataFrame(res, columns=['ts', 'open', 'high', 'low', 'close', 'vol', 'ct', 'qa', 'nt', 'tbv', 'tqv', 'i'])
        df['close'] = df['close'].astype(float)
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

async def send_signal(msg):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode='Markdown')
        print("✅ سیگنال هاتە ناردن بۆ چەناڵی!")
    except Exception as e:
        print(f"❌ شاشییەک د ناردنێ دا: {e}")

async def main():
    print(f"🚀 بوتێ Prime_Vortex دەست ب کار بوو ل سەر {SYMBOL}...")
    last_signal = None

    while True:
        try:
            df = get_data(SYMBOL, INTERVAL)
            if df is not None:
                df['RSI'] = ta.rsi(df['close'], length=14)
                rsi = df['RSI'].iloc[-1]
                price = df['close'].iloc[-1]

                print(f"Price: {price} | RSI: {rsi:.2f}")

                # مەرجێ کڕینێ (Oversold)
                if rsi < 30 and last_signal != 'buy':
                    msg = f"🔵 **Prime_Vortex: BUY SIGNAL**\n\n🪙 Asset: #{SYMBOL}\n💰 Entry Price: ${price}\n📉 RSI Level: {rsi:.2f}\n⏱ Timeframe: {INTERVAL}\n\n⚠️ *Auto-generated signal*"
                    await send_signal(msg)
                    last_signal = 'buy'

                # مەرجێ فرۆشتنێ (Overbought)
                elif rsi > 70 and last_signal != 'sell':
                    msg = f"🟠 **Prime_Vortex: SELL SIGNAL**\n\n🪙 Asset: #{SYMBOL}\n💰 Exit Price: ${price}\n📈 RSI Level: {rsi:.2f}\n⏱ Timeframe: {INTERVAL}\n\n⚠️ *Auto-generated signal*"
                    await send_signal(msg)
                    last_signal = 'sell'

        except Exception as e:
            print(f"Main loop error: {e}")

        await asyncio.sleep(60) # پشکنین خولەک ب خولەک

if __name__ == "__main__":
    asyncio.run(main())
