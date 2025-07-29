from binance.client import Client
from config import BINANCE_API_KEY, BINANCE_API_SECRET, SYMBOL, BASE_ASSET, QUOTE_ASSET

client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

def get_balance(asset):
    b = client.get_asset_balance(asset=asset)
    return float(b['free']) if b else 0.0

def get_price():
    return float(client.get_symbol_ticker(symbol=SYMBOL)['price'])

def buy_eth(amount_usdc):
    price = get_price()
    qty = round(amount_usdc / price, 5)
    print(f"[BUY] {qty} ETH per {amount_usdc:.2f} USDC")
    return client.order_market_buy(symbol=SYMBOL, quantity=qty)

def sell_all_eth():
    qty = round(get_balance(BASE_ASSET), 5)
    if qty >= 0.001:
        print(f"[SELL] {qty} ETH venduti")
        return client.order_market_sell(symbol=SYMBOL, quantity=qty)
    print("[SELL] Nessun ETH da vendere")
    return None
