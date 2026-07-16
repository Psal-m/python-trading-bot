import yfinance as yf
import openpyxl
import time
import math
import os
from datetime import datetime
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

# FILE
def xl(sts, price, qty):
    file = 'xl.xlsx'
    if not os.path.exists(file):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(['time', 'stats', 'price', 'amount'])
    else:
        wb = openpyxl.load_workbook(file)
        ws = wb.active
    ws.append([str(datetime.now()), sts, price, qty])
    wb.save(file)
    
# Connect
key1 = ''
key2 = ''
client = TradingClient(key1, key2, paper=True)

# Editables
sts = 'SELL'
b_price = 0.0
buy_tg = 0.0
sell_tg = 0.0
amount = 0.0

# Fetch
symbol = ''

while True:
    try:
        tracker = yf.Ticker(symbol)
        data = tracker.history(period='1d')
        price = data['Close'].iloc[-1]

        # Buy/selling
        if sts == 'SELL':
            if price <= buy_tg:
                client.submit_order(MarketOrderRequest(symbol=symbol, qty=amount, side=OrderSide.BUY, time_in_force=TimeInForce.GTC))
                sts = 'BUY'
                b_price = price
                xl('BUY', price, amount)

        elif sts == 'BUY':
            if price >= sell_tg:
                client.submit_order(MarketOrderRequest(symbol=symbol, qty=amount, side=OrderSide.SELL, time_in_force=TimeInForce.GTC))
                sts = 'SELL'
                xl('SELL', price, amount)
    
    except Exception as e:
        print(f"An error occurred: {e}")

    time.sleep(10)
