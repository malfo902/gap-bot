from flask import Flask, request, jsonify
from binance.client import Client
from config import BINANCE_API_KEY, BINANCE_API_SECRET
import datetime

app = Flask(__name__)
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

def get_futures_balance_usdt():
    try:
        balances = client.futures_account_balance()
        for b in balances:
            if b['asset'] == 'USDT':
                return float(b['balance'])
    except Exception as e:
        print(f"Errore nel recupero del saldo: {e}")
        return None

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    now = datetime.datetime.now(datetime.UTC).isoformat()

    print("\n📩 Segnale ricevuto:")
    print(f"🕒 {now}")
    print(f"Asset: {data.get('asset')}")
    print(f"TF: {data.get('timeframe')}")
    print(f"Evento: {data.get('event')}")
    print(f"TradingView time: {data.get('timestamp')}")

    event = data.get("event")
    if event not in ["gap_up", "gap_down", "gap_closed"]:
        return jsonify({"status": "ignored", "reason": "evento non valido"})

    if event == "gap_closed":
        print("✅ CHIUSURA posizione (da implementare)")
        return jsonify({"status": "ok", "message": "Gap chiuso"})

 usdt_balance = get_futures_balance_usdt()
    if usdt_balance is None:
        return jsonify({"status": "errore", "message": "saldo non disponibile"})

    investment = usdt_balance * 0.04  # 4%
    symbol = "ETHUSDT"
    side = Client.SIDE_SELL if event == "gap_up" else Client.SIDE_BUY

    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=Client.ORDER_TYPE_MARKET,
            quantity=round(investment / client.futures_symbol_ticker(symbol=symbol)['price'], 3)
        )
        print(f"📤 Ordine inviato: {side} {symbol} con {investment:.2f} USDT")
        return jsonify({"status": "success", "order": order})
    except Exception as e:
        print(f"❌ Errore nell'invio dell'ordine: {e}")
        return jsonify({"status": "errore", "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
