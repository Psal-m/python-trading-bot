import time
import math
import yfinance as yf
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
#key

API='actual_key'
SK='actual_secret'
tc=TradingClient(API,SK,paper=True)
#fetch
sym = 'BTC-USD'
order_sym = 'BTCUSD'
status = "SEARCHING"
buy_price = 0.0
#proc
dip = 0.005
profit = 0.0075

print("Running...")

while True:
    try:
        data = yf.Ticker(sym)
        live = data.fast_info['lastPrice']
        
        print(f"Price: ${live:.2f} | Status: {status}")
        
        if status == "SEARCHING":
            target_buy = live * (1 - dip)
            if live >= target_buy:
                print("Buying...")
                req = MarketOrderRequest(
                    symbol=order_sym,
                    qty=round(9000/live,4),
                    side=OrderSide.BUY,
                    time_in_force=TimeInForce.GTC
                )
                tc.submit_order(order_data=req)
                buy_price = live
                status = "HOLDING"
        
        elif status == "HOLDING":
            target_sell = buy_price * (1 + profit)
            if live >= target_sell:
                print("Selling...")
                req = MarketOrderRequest(
                    symbol=order_sym,
                    qty=round(9000/live,4),
                    side=OrderSide.SELL,
                    time_in_force=TimeInForce.GTC
                )
                tc.submit_order(order_data=req)
                status = "SEARCHING"

    except Exception as e:
        print(f"Error: {e}")
        
    time.sleep(10)
