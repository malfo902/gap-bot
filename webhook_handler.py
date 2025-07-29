from flask import Flask, request, jsonify
from config import WEBHOOK_SECRET
from bot_gap import handle_gap_down, handle_gap_closed, track_prices

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    auth = request.headers.get("Authorization")
    if auth != f"Bearer {WEBHOOK_SECRET}":
        return jsonify({"error": "Accesso negato"}), 403

    data = request.get_json()
    if not data or "type" not in data or "gap_base" not in data:
        return jsonify({"error": "Dati incompleti"}), 400

    event_type = data["type"]
    gap_base = float(data["gap_base"])

    if event_type == "GAP_DOWN":
        handle_gap_down(gap_base)
    elif event_type == "GAP_CLOSED":
        handle_gap_closed(gap_base)
    else:
        return jsonify({"error": "Tipo evento non supportato"}), 400

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    import threading
    threading.Thread(target=track_prices, daemon=True).start()
    app.run(host="0.0.0.0", port=8000)
