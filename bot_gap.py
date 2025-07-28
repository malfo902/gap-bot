from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    now = datetime.datetime.utcnow().isoformat()
    print("\n📩 Segnale ricevuto:")
    print(f"🕒 {now}")
    print(f"Asset: {data.get('asset')}")
    print(f"TF: {data.get('timeframe')}")
    print(f"Evento: {data.get('event')}")
    print(f"TradingView time: {data.get('timestamp')}")

    if data.get("event") == "gap_up":
        print("🔴 SHORT ETH")
    elif data.get("event") == "gap_down":
        print("🟢 LONG ETH")
    elif data.get("event") == "gap_closed":
        print("✅ CHIUSURA posizione")

    return jsonify({"status": "received", "event": data.get("event")})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
