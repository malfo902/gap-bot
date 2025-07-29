import os

BINANCE_API_KEY = os.getenv("")
BINANCE_API_SECRET = os.getenv("")

SYMBOL = "ETHUSDC"
QUOTE_ASSET = "USDC"
BASE_ASSET = "ETH"

TRADE_PERCENTAGE = 0.04
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

POLL_INTERVAL = 10  # secondi tra controlli prezzo
