import os

BINANCE_API_KEY = os.getenv("cyF4T8OTEomDm5L8nBX9AweNjOwkLWoObDn8uzlhSSpwS0MuFtyJGEaIe283bSQZ")
BINANCE_API_SECRET = os.getenv("NhKbFEuTVe9TXVa9fuj0Q2JJP1af5dfjuII3oMJ7uRp5ZhtrTwTi60tL5VJn0Bkf")

# Asset configurazione
SYMBOL = "ETHUSDC"
QUOTE_ASSET = "USDC"
BASE_ASSET = "ETH"

# Percentuale di investimento per ogni livello (es: 4% del saldo USDC disponibile)
TRADE_PERCENTAGE = 0.04

# Sicurezza e webhook
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

# Frequenza del controllo prezzo (in secondi)
POLL_INTERVAL = 10

