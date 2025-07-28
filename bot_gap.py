from flask import Flask, request, jsonify
import datetime
import json

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        raw_data = request.data.decode('utf-8')
        print("\n📩 Webhook ricevuto!")
        print(f"Contenuto raw: {raw_data}")

        data = json.loads(raw_data)

        now = datetime.datetime.utcnow().isoformat()
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

    except Exception as e:
        print(f"⚠️ Errore nel webhook: {e}")
        return "Invalid request", 400


@app.route('/debug', methods=['GET'])
def debug():
    print("✅ /debug ping ricevuto")
    return "Bot attivo", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
