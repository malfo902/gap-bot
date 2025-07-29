# binance_handler.py

from binance.client import Client
from config import BINANCE_API_KEY, BINANCE_API_SECRET, SYMBOL, BASE_ASSET, QUOTE_ASSET

client = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_API_SECRET)

def get_balance(asset):
    bal = client.get_asset_balance(asset=asset)
    return float(bal['free']) if bal else 0.0

def get_price():
    return float(client.get_symbol_ticker(symbol=SYMBOL)['price'])

def buy_eth_usdc(amount_usdc):
    price = get_price()
    qty = round(amount_usdc / price, 5)
    return client.order_market_buy(symbol=SYMBOL, quantity=qty)

def sell_all_eth():
    eth_qty = round(get_balance(BASE_ASSET), 5)
    if eth_qty >= 0.001:
        return client.order_market_sell(symbol=SYMBOL, quantity=eth_qty)
    return None
